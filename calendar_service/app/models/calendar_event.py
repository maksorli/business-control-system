from app.core.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from uuid import UUID, uuid4
from datetime import datetime

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    type: Mapped[str]  # task, meeting
    related_id: Mapped[UUID]
    user_id: Mapped[UUID]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)