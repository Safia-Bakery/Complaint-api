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

class ComplaintProducts(Base):
    __tablename__ = "complaint_products"
    id = Column(BIGINT, primary_key=True, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("iiko_products.id"))
    product = relationship("IikoProducts", back_populates="complaint_product")
    complaint_id = Column(BIGINT, ForeignKey("complaints.id"))
    complaint = relationship("Complaints", back_populates="complaint_product")

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())