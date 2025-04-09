from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import meetings
from app.core.init_db import init_db
from app.kafka.topic_init import create_kafka_topics

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await create_kafka_topics()
    yield

app = FastAPI(
    title="Meeting Service",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(meetings.router)