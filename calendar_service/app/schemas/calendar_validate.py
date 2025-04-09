from pydantic import BaseModel 
from uuid import UUID
from datetime import datetime

class CalendarValidateRequest(BaseModel):
    user_id: UUID
    start_time: datetime
    end_time: datetime