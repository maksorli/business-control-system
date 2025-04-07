from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from typing_extensions import Literal

class CurrentUser(BaseModel):
    id: UUID
    role: Literal["admin", "manager", "employee"]
    team_id: Optional[UUID]= None
    token: Optional[str] = None
