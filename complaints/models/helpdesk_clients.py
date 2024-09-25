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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import SessionLocal, Base



class HelpDeskClients(Base):
    __tablename__ = "help_desk_clients"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1)
    telegram_id = Column(BIGINT, nullable=True)
    help_desk = relationship("HelpDeskChats", back_populates="help_desk_client")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    class Config:
        orm_mode = True