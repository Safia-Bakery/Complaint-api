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
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import pytz
import uuid

from hrcomplaint.models.hr_model import Base


timezonetash = pytz.timezone("Asia/Tashkent")


class Countries(Base):
    __tablename__ = "countries"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, nullable=True)
    service_id = Column(String,nullable= True)
    quality_id = Column(String,nullable= True)
    status = Column(Integer, default=1)
    callcenter_id = Column(String,nullable= True)
    subcategory = relationship("Subcategories",back_populates="country")
    branch = relationship("Branchs",back_populates="country")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Categories(Base):
    __tablename__ = "categories"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String)
    status = Column(Integer, default=1)
    subcategory = relationship("Subcategories",back_populates="category")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Subcategories(Base):
    __tablename__ = "subcategories"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(BIGINT, ForeignKey("categories.id"))
    category = relationship("Categories",back_populates="subcategory")
    country_id = Column(BIGINT, ForeignKey("countries.id"))
    country = relationship("Countries",back_populates="subcategory")
    complaint = relationship("Complaints",back_populates="subcategory")
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())





class Branchs(Base):
    __tablename__ = "branchs"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String)
    country_id = Column(BIGINT, ForeignKey("countries.id"))
    country = relationship("Countries",back_populates="branch")
    password = Column(String, nullable=True)
    status = Column(Integer, default=1)
    complaint = relationship("Complaints",back_populates="branch")
    rating = relationship("Ratings",back_populates="branch")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Clients(Base):
    __tablename__ = "clients"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String)
    status = Column(Integer, default=1)
    complaint = relationship("Complaints",back_populates="client")
    rating = relationship("Ratings",back_populates="client")
    branch_id = Column(BIGINT, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(BIGINT, primary_key=True, index=True)
    rating = Column(Integer, default=0)
    branch_id = Column(BIGINT, ForeignKey("branchs.id"))
    branch = relationship("Branchs",back_populates="rating")
    client_id = Column(BIGINT, ForeignKey("clients.id"),nullable=True)
    client = relationship("Clients",back_populates="rating")
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Complaints(Base):
    __tablename__ = "complaints"
    id = Column(BIGINT, primary_key=True, index=True)
    product_name = Column(String,nullable=True)
    client_name = Column(String,nullable=True)
    client_number = Column(String,nullable=True)
    client_gender = Column(String,nullable=True)
    date_purchase = Column(DateTime,nullable=True)
    date_return = Column(DateTime,nullable=True)
    comment = Column(String, nullable=True)
    otk_status = Column(Integer,default=0)
    status = Column(Integer, default=0)
    is_client = Column(Boolean, default=False)
    corrections = Column(String, nullable=True)
    autonumber = Column(String, nullable=True)
    expense = Column(Float, nullable=True)
    subcategory_id = Column(BIGINT, ForeignKey("subcategories.id"))
    subcategory = relationship("Subcategories",back_populates="complaint")
    branch_id = Column(BIGINT, ForeignKey("branchs.id"))
    branch = relationship("Branchs",back_populates="complaint")
    status = Column(Integer, default=1)
    file = relationship("Files",back_populates="complaint")
    communication = relationship("Communications",back_populates="complaint")
    client_id = Column(BIGINT, ForeignKey("clients.id"),nullable=True)
    client = relationship("Clients",back_populates="complaint")
    changes = Column(JSONB, nullable=True)
    updated_by = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Files(Base):
    __tablename__ = "files"
    id = Column(BIGINT, primary_key=True, index=True)
    url = Column(String, nullable=True)
    complaint_id = Column(BIGINT, ForeignKey("complaints.id"))
    complaint = relationship("Complaints",back_populates="file")
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Communications(Base):
    __tablename__ = "communications"
    id = Column(BIGINT, primary_key=True, index=True)
    complaint_id = Column(BIGINT, ForeignKey("complaints.id"))
    complaint = relationship("Complaints",back_populates="communication")
    user_id = Column(BIGINT, ForeignKey("users.id"), nullable=True)
    user = relationship("Users",back_populates="communication")
    text = Column(String, nullable=True)
    status = Column(Integer, default=1)
    url=  Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

