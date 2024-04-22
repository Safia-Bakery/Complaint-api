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



