from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from app.core.base import Base


class TaskStatus(enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.OPEN)
    due_date: Mapped[datetime]

    assignee_id: Mapped[uuid.UUID]
    team_id: Mapped[uuid.UUID]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    comments: Mapped[list["Comment"]] = relationship(back_populates="task", cascade="all, delete-orphan")

