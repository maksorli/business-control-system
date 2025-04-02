from fastapi import Depends
from app.core.database import get_session
from app.repositories.team_repository import TeamRepository

async def get_user_repository(session=Depends(get_session)):
    return TeamRepository(session)