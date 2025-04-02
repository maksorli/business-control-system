from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TeamCreate(BaseModel):
    name: str
    description: str

class TeamOut(BaseModel):
    id: UUID
    name: str
    description: str
    invite_code: str
    created_at: datetime

    class Config:
        orm_mode = True


class JoinTeamRequest(BaseModel):
    invite_code: str
