from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from complaints.schemas.files import GetFiles
from complaints.schemas.complaint_stampers import GetComplaintStampers
from complaints.schemas.subcategories import GetSubCategories


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



class V2UpdateComplaints(BaseModel):
    product_name: Optional[str] = None
    client_name: Optional[str] = None
    client_number: Optional[str] = None
    client_gender: Optional[str] = None
    date_purchase: Optional[datetime] = None
    date_return: Optional[datetime] = None
    is_returned: Optional[bool] = None
    producer_guilty: Optional[bool] = None
    comment: Optional[str] = None
    otk_status: Optional[int] = None
    deny_reason: Optional[str] = None
    status: Optional[int] = None
    corrections: Optional[str] = None
    autonumber: Optional[str] = None
    subcategory_id: Optional[int] = None
    branch_id: Optional[int] = None
    expense: Optional[float] = None
    first_response: Optional[str] = None
    second_response: Optional[str] = None
    id : int


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
    first_response: Optional[str] = None
    second_response: Optional[str] = None
    first_response_time: Optional[datetime] = None
    second_response_time: Optional[datetime] = None
    # file : Optional[list[GetFiles]] = None

    class Config:
        orm_mode = True

class V2GetOneComplaint(BaseModel):
    product_name: Optional[str] = None
    client_name: Optional[str] = None
    client_number: Optional[str] = None
    date_purchase: Optional[datetime] = None
    date_return: Optional[datetime] = None
    comment: Optional[str] = None
    subcategory_id: Optional[int] = None
    subcategory: Optional[GetSubCategories] = None
    branch_id: Optional[int] = None
    expense: Optional[float] = None
    complaint_product : Optional[list[ComplaintProducts]] = None
    client_id: Optional[int] = None
    file : Optional[list[GetFiles]] = None
    first_response: Optional[str] = None
    second_response: Optional[str] = None
    first_response_time: Optional[datetime] = None
    second_response_time: Optional[datetime] = None
    complaint_stamp : Optional[list[GetComplaintStampers]] = None
    certificate: Optional[str]=None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True


