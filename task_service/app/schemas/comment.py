from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    user_id: UUID
    task_id: UUID


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
