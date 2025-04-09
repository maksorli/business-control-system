from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

from services_config import services  # Словарь: { "users": "http://users_service:8000/openapi.json", ... }

app = FastAPI(
    title="API Gateway",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# 🔹 Объединённая OpenAPI-схема
@app.get("/openapi-merged.json")
async def merged_openapi():
    merged = {
        "openapi": "3.0.0",
        "info": {"title": "Merged API", "version": "1.0.0"},
        "paths": {},
        "components": {"schemas": {}},
        "tags": []
    }

    async with httpx.AsyncClient() as client:
        for name, url in services.items():
            try:
                response = await client.get(url)
                schema = response.json()
                tag_name = name.capitalize()

                for path, path_item in schema.get("paths", {}).items():
                    merged["paths"][f"/{name}{path}"] = path_item

                merged["components"]["schemas"].update(
                    schema.get("components", {}).get("schemas", {})
                )

                merged["tags"].append({"name": tag_name})
            except Exception as e:
                print(f"[Gateway] ❌ Error loading {name}: {e}")

    return merged

# 🔹 Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
      <head>
        <title>API Gateway Docs</title>
        <link href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" rel="stylesheet" />
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script>
          SwaggerUIBundle({
            url: "/openapi-merged.json",
            dom_id: "#swagger-ui"
          });
        </script>
      </body>
    </html>
    """)

# 🔹 Прокси-запросы: перенаправляем запросы от /users/... → http://users_service:8000/...
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in services:
        return JSONResponse({"detail": f"Service '{service}' not found"}, status_code=404)

    base_url = services[service].replace("/openapi.json", "")  # http://users_service:8000
    target_url = f"{base_url}/{path}"
    req_body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers={key: value for key, value in request.headers.items() if key.lower() != "host"},
                content=req_body,
                params=request.query_params
            )
            return JSONResponse(status_code=resp.status_code, content=resp.json())
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
