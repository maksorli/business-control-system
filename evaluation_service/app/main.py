from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import async_engine
from app.core.base import Base
from app.api import evaluations   


@asynccontextmanager
async def lifespan(app: FastAPI):
     
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Evaluation Service",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(evaluations.router)
