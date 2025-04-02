from fastapi import Depends
from app.core.database import get_session
from app.repositories.user_repository import UserRepository

async def get_user_repository(session=Depends(get_session)):
    return UserRepository(session)