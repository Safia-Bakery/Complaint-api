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


class ComplaintStampers(Base):
    __tablename__ = "complaint_stampers"
    id = Column(BIGINT, primary_key=True, index=True)

    user_id = Column(BIGINT, ForeignKey("users.id"))
    user = relationship("Users", back_populates="complaint_stamp")
    complaint_id = Column(BIGINT, ForeignKey("complaints.id"))
    complaint = relationship("Complaints", back_populates="complaint_stamp")
    status = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    class Config:
        orm_mode = True