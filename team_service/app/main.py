from fastapi import FastAPI
from contextlib import asynccontextmanager
 
from app.api import team

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(team.router)