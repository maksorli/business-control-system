from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.core.base import Base
from datetime import datetime


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    invite_code = Column(String, unique=True)  
    created_at = Column(DateTime, default=datetime.utcnow)


