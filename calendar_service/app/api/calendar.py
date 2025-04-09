from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from app.core.database import get_session
from app.schemas.calendar_event import CalendarEventRead
from app.schemas.calendar_validate import CalendarValidateRequest
from app.repositories.calendar_repository import CalendarRepository

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/day/{day}", response_model=list[CalendarEventRead])
async def get_day(day: date, session: AsyncSession = Depends(get_session)):
    repo = CalendarRepository(session)
    return await repo.get_by_day(day)

@router.get("/month/{year}/{month}", response_model=list[CalendarEventRead])
async def get_month(year: int, month: int, session: AsyncSession = Depends(get_session)):
    repo = CalendarRepository(session)
    return await repo.get_by_month(year, month)

@router.post("/validate", response_model=dict)
async def validate_user_availability(
    data: CalendarValidateRequest,
    session: AsyncSession = Depends(get_session)
):
    repo = CalendarRepository(session)
    is_available = await repo.is_user_available(
        user_id=data.user_id,
        start_time=data.start_time,
        end_time=data.end_time
    )
    return {"available": is_available}