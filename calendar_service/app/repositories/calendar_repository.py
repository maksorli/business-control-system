# app/repositories/calendar_repository.py
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar_event import CalendarEventCreate

class CalendarRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CalendarEventCreate) -> CalendarEvent:
        event = CalendarEvent(**data.model_dump())
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_by_day(self, day: date):
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        result = await self.session.execute(
            select(CalendarEvent).where(CalendarEvent.start_time >= start, CalendarEvent.start_time <= end)
        )
        return result.scalars().all()

    async def get_by_month(self, year: int, month: int):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        result = await self.session.execute(
            select(CalendarEvent).where(CalendarEvent.start_time >= start, CalendarEvent.start_time < end)
        )
        return result.scalars().all()
