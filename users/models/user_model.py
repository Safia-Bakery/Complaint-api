from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import pytz
import uuid

from complaints.models.request_model import Communications,Base


timezonetash = pytz.timezone("Asia/Tashkent")


class Pages(Base):
    __tablename__ = "pages"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1)
    action = relationship("Actions",back_populates="page")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Actions(Base):
    __tablename__ = "actions"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1)
    page_id = Column(BIGINT, ForeignKey("pages.id"))
    page = relationship("Pages",back_populates="action")
    permission = relationship("Permissions",back_populates="action")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Roles(Base):
    __tablename__ = "roles"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer, default=1)
    permission = relationship("Permissions",back_populates="role")
    user = relationship("Users",back_populates="role")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(BIGINT, primary_key=True, index=True)
    action_id = Column(BIGINT, ForeignKey("actions.id"))
    action = relationship("Actions",back_populates="permission")
    role_id = Column(BIGINT, ForeignKey("roles.id"))
    role = relationship("Roles",back_populates="permission")
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



# this is models of userss
class Users(Base):  
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    status = Column(Integer,default=0)
    role_id = Column(BIGINT, ForeignKey("roles.id"))
    role = relationship("Roles",back_populates="user")
    hrcommunication = relationship("Hrcommunications",back_populates="user")
    communication = relationship("Communications",back_populates="user")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


