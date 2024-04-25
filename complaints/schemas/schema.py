from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID



class CreateCountry(BaseModel):
    name: Optional[str]=None
    code:Optional[str]=None
    status: Optional[int]=None
    service_id: Optional[str]=None
    quality_id: Optional[str]=None
    callcenter_id: Optional[str]=None
    class Config:
        orm_mode = True



class UpdateCountry(BaseModel):
    id:int
    name: Optional[str]=None
    code:Optional[str]=None
    status: Optional[int]=None
    service_id: Optional[str]=None
    quality_id: Optional[str]=None
    callcenter_id: Optional[str]=None
    class Config:
        orm_mode = True



class Country(BaseModel):
    id:int
    name: Optional[str]=None
    code:Optional[str]=None
    status: Optional[int]=None
    service_id: Optional[str]=None
    quality_id: Optional[str]=None
    callcenter_id: Optional[str]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class CreateCategory(BaseModel):
    name: Optional[str]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True
    
class UpdateCategory(BaseModel):
    id:int
    name: Optional[str]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True

class Category(BaseModel):
    id:int
    name: Optional[str]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class CreateSubCategory(BaseModel):
    name: Optional[str]=None
    category_id: Optional[int]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True

class UpdateSubCategory(BaseModel):
    id:int
    name: Optional[str]=None
    category_id: Optional[int]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True

class SubCategory(BaseModel):
    id:int
    name: Optional[str]=None
    category_id: Optional[int]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class CreateBranch(BaseModel):
    name: Optional[str]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True



class UpdateBranch(BaseModel):
    id:int
    name: Optional[str]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    password:Optional[bool]=False
    class Config:
        orm_mode = True

class Branchs(BaseModel):
    id:int
    name: Optional[str]=None
    country_id: Optional[int]=None
    status: Optional[int]=None
    password:Optional[str]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True



class Files(BaseModel):
    id:int
    url: Optional[str]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True

class Clients(BaseModel):
    id:int
    name: Optional[str]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True

class Complaints(BaseModel):
    id:int
    product_name: Optional[str]=None
    client_name: Optional[str]=None
    client_number: Optional[str]=None
    client_gender: Optional[str]=None
    date_purchase: Optional[datetime]=None
    date_return: Optional[datetime]=None
    comment: Optional[str]=None
    otk_status: Optional[int]=None
    status: Optional[int]=None
    is_client: Optional[bool]=None
    corrections: Optional[str]=None
    autonumber: Optional[str]=None
    subcategory_id: Optional[int]=None
    branch_id: Optional[int]=None
    subcategory: Optional[SubCategory]=None
    branch: Optional[Branchs]=None
    file: Optional[list[Files]]=None
    changes: Optional[Dict]=None
    client_id: Optional[int]=None
    client: Optional[Clients]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True




class UpdateComplaint(BaseModel):
    id:int
    product_name: Optional[str]=None
    client_name: Optional[str]=None
    client_number: Optional[str]=None
    client_gender: Optional[str]=None
    date_purchase: Optional[datetime]=None
    date_return: Optional[datetime]=None
    comment: Optional[str]=None
    otk_status: Optional[int]=None
    status: Optional[int]=None
    corrections: Optional[str]=None
    autonumber: Optional[str]=None
    subcategory_id: Optional[int]=None
    branch_id: Optional[int]=None
    expense: Optional[float]=None


    