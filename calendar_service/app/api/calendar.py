from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from app.core.database import get_session
from app.schemas.calendar_event import CalendarEventRead
from app.repositories.calendar_repository import CalendarRepository

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/day/{day}", response_model=list[CalendarEventRead])
async def get_day(day: date, session: AsyncSession = Depends(get_session)):
    repo = CalendarRepository(session)
    return await repo.get_by_day(day)

@router.get("/month/{year}/{month}", response_model=list[CalendarEventRead])
async def get_month(year: int, month: int, session: AsyncSession = Depends(get_session)):
    repo = CalendarRepository(session)
    return await repo.get_by_month(year, month)
