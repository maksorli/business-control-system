import httpx
from fastapi import HTTPException

async def validate_team_id(team_id: str, token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://team_service:8000/teams/{team_id}",
                headers=headers
            )
            if response.status_code == 404:
                raise HTTPException(status_code=400, detail="Team not found")
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Team service is unavailable")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Error contacting team service")