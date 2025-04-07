from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    status: TaskStatus = TaskStatus.OPEN
    assignee_id: UUID
    team_id: UUID


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[UUID] = None


class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
