# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.init_db import init_db  # твоя функция создания таблиц
from app.api import users
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting... Initializing DB...")
    await init_db()
    print("✅ DB initialized")
    yield
    print("🛑 App shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)