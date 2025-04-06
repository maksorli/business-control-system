from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str = Field(..., example="HR")
    team_id: UUID


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = None


class DepartmentRead(DepartmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
