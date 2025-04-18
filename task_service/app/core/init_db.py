from app.core.database import async_engine
from app.core.base import Base


from app.models import task, comment

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
