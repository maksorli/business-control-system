from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class MeetingBase(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    team_id: UUID
    organizer_id: UUID

class MeetingCreate(MeetingBase):
    participant_ids: List[UUID]

class MeetingUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    participant_ids: Optional[List[UUID]]

class MeetingRead(MeetingBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
