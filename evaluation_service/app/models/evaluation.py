from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4 

from app.core.base import Base


class TaskEvaluation(Base):
    __tablename__ = "task_evaluations"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    task_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    assignee_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    reviewer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    score_speed: Mapped[int] = mapped_column(nullable=False)
    score_quality: Mapped[int] = mapped_column(nullable=False)
    score_completeness: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
