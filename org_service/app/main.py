from fastapi import FastAPI
from app.models import department
from app.core.init_db import init_db  
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import departments

app = FastAPI(title="Organizational Structure Service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(departments.router)



 