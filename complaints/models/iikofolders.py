import pytz
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
)
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from database import SessionLocal, Base


class IikoFolders(Base):
    __tablename__ = "iiko_folders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())





