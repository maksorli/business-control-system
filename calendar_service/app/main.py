from fastapi import FastAPI
from app.api.calendar import router
from contextlib import asynccontextmanager
from app.core.init_db import init_db
from app.kafka.comsumer import consume_events
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    asyncio.create_task(consume_events())
    yield

app = FastAPI(title="Calendar Service", lifespan=lifespan)
app.include_router(router)
