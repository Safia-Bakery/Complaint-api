import pytz
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    BIGINT,
)
# from users.models.user_model import Users

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import pytz
import uuid

from database import SessionLocal, Base

timezonetash = pytz.timezone("Asia/Tashkent")

class Hrspheras(Base):
    __tablename__ = "hrspheras"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    name_uz = Column(String, nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    hrcategory = relationship("HrCategories",back_populates="hrsphere")
    hrcomplaint = relationship("Hrcomplaints",back_populates="hrsphere")
    hrquestion = relationship("Hrquestions",back_populates="hrsphere")


class HrCategories(Base):
    __tablename__ = "hrcategories"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    name_uz = Column(String, nullable=True)
    status = Column(Integer, default=1)
    hrsphere_id = Column(BIGINT, ForeignKey("hrspheras.id"),nullable=True)
    hrsphere = relationship("Hrspheras",back_populates="hrcategory")
    hrcomplaint = relationship("Hrcomplaints",back_populates="hrcategory")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Hrcomplaints(Base):
    __tablename__ = "hrcomplaints"
    id = Column(BIGINT, primary_key=True, index=True)
    complaint = Column(String, nullable=True)
    category_id = Column(BIGINT, ForeignKey("hrcategories.id"),nullable=True)
    hrcategory = relationship("HrCategories",back_populates="hrcomplaint")
    sphere_id = Column(BIGINT, ForeignKey("hrspheras.id"))
    hrsphere = relationship("Hrspheras",back_populates="hrcomplaint")
    hrcommunication = relationship("Hrcommunications",back_populates="hrcomplaint")
    hrclient_id = Column(BIGINT, ForeignKey("hrclients.id"))
    hrclient = relationship("Hrclients",back_populates="hrcomplaint")
    hrtype = Column(Integer, nullable=True)
    status = Column(Integer, default=1)
    deny_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Hrclients(Base):
    __tablename__ = "hrclients"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1)
    sphere = Column(Integer, nullable=True)
    lang = Column(Integer, nullable=True)
    hrcomplaint = relationship("Hrcomplaints",back_populates="hrclient")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Hrcommunications(Base):
    __tablename__ = "hrcommunications"
    id = Column(BIGINT, primary_key=True, index=True)
    hrcomplaint_id = Column(BIGINT,ForeignKey('hrcomplaints.id'),nullable=True)
    hrcomplaint = relationship("Hrcomplaints",back_populates="hrcommunication")
    text = Column(String, nullable=True)
    status = Column(Integer, default=0)
    url = Column(String, nullable=True)
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=True)
    user = relationship("Users",back_populates="hrcommunication")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Hrquestions(Base):
    __tablename__ = "hrquestions"
    id = Column(BIGINT, primary_key=True, index=True)
    question_uz = Column(String, nullable=True)
    question_ru = Column(String, nullable=True)
    sphere_id = Column(BIGINT, ForeignKey("hrspheras.id"))
    hrsphere = relationship("Hrspheras",back_populates="hrquestion")
    answer_uz = Column(String, nullable=True)
    answer_ru = Column(String, nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())




class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(BIGINT, primary_key=True)
    text = Column(String, nullable=False)
    created_by = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    user = relationship("Users", back_populates="notifications")
    scheduled_at = Column(DateTime(timezone=True))
    status = Column(Integer, default=0)
    receivers_sphere = Column(ARRAY(Integer))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

