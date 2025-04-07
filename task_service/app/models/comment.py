from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
import uuid

from app.core.base import Base
from app.models.task import Task

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[uuid.UUID]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    task: Mapped["Task"] = relationship(back_populates="comments")
