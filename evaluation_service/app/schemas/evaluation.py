from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class EvaluationBase(BaseModel):
    task_id: UUID
    assignee_id: UUID
    reviewer_id: UUID
    score_speed: int = Field(..., ge=0, le=10)
    score_quality: int = Field(..., ge=0, le=10)
    score_completeness: int = Field(..., ge=0, le=10)


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationRead(EvaluationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True  
