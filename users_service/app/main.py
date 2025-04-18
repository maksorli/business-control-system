from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.init_db import init_db  
from app.api import users
@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)