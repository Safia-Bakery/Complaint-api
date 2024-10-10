from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from complaints.schemas.files import GetFiles


class ProductsGet(BaseModel):
    id: UUID
    name: str
    class Config:
        orm_mode = True


class ComplaintProducts(BaseModel):
    product_id: UUID
    complaint_id: int
    product : Optional[ProductsGet] = None
    class Config:
        orm_mode = True



class V2CreateComplaints(BaseModel):
    files: Optional[list[str]] = None
    product_name: Optional[str] = None
    client_name: Optional[str] = None
    client_number: Optional[str] = None
    date_purchase: Optional[datetime] = None
    date_return: Optional[datetime] = None
    comment: Optional[str] = None
    subcategory_id: Optional[int] = None
    branch_id: Optional[int] = None
    expense: Optional[float] = None
    products : Optional[list[UUID]] = None
    client_id: Optional[int] = None
    class Config:
        orm_mode = True


class V2ComplaintsGet(BaseModel):
    product_name: Optional[str] = None
    client_name: Optional[str] = None
    client_number: Optional[str] = None
    date_purchase: Optional[datetime] = None
    date_return: Optional[datetime] = None
    comment: Optional[str] = None
    subcategory_id: Optional[int] = None
    branch_id: Optional[int] = None
    expense: Optional[float] = None
    complaint_product : Optional[list[ComplaintProducts]] = None
    client_id: Optional[int] = None
    file : Optional[list[GetFiles]] = None

    class Config:
        orm_mode = True


