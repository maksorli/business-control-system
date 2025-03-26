# app/core/init_db.py
from app.core.database import async_engine
from app.core.base import Base

# 👇 Импортируем ВСЕ модели, чтобы таблицы попали в metadata
from app.models import user

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
