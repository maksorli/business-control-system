from sqlalchemy import Column, String 
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.core.base import Base
 


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    invite_code = Column(String, unique=True)  # например: "XYZ123"