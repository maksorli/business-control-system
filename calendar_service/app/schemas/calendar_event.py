from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class CalendarEventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    type: str
    related_id: UUID
    user_id: UUID

class CalendarEventRead(CalendarEventCreate):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
