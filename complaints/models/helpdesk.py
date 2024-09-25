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



class HelpDeskChats(Base):
    __tablename__ = "help_desk_chats"
    id = Column(BIGINT, primary_key=True, index=True)
    comment = Column(String, nullable=True)
    file = Column(String, nullable=True)
    message_id = Column(BIGINT, nullable=True)
    status = Column(Integer, default=1)
    is_client = Column(Boolean, default=True)
    help_desk_client_id = Column(BIGINT, ForeignKey("help_desk_clients.id"))
    help_desk_client = relationship("HelpDeskClients", back_populates="help_desk")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    class Config:
        orm_mode = True



