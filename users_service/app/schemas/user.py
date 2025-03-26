from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    invite_code: Optional[str] = None
    role: Optional[RoleEnum] = RoleEnum.employee
    

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: RoleEnum
    team_id: Optional[UUID]

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    invite_code: Optional[str] = None
