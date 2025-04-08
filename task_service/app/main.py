from fastapi import FastAPI
from app.models import task
from app.models import comment
from app.core.init_db import init_db  
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import tasks, comments
from app.kafka.topic_init import create_kafka_topics
 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_kafka_topics()
    await init_db()
    yield

app = FastAPI(
    title="Task Service",
    version="1.0.0",
    lifespan=lifespan,
)

 
app.include_router(tasks.router)
app.include_router(comments.router)