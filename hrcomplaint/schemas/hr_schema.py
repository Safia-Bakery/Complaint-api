from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas.user_sch import User

class Sphere(BaseModel):
    id:int
    name: Optional[str]=None
    status: int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True



class SphereCreate(BaseModel):
    name: Optional[str]=None
    status: Optional[int]=1
    class Config:
        orm_mode = True

class QuestionsCreate(BaseModel):
    question_uz: Optional[str]=None
    question_ru: Optional[str]=None
    answer_uz: Optional[str]=None
    sphere_id:int
    answer_ru: Optional[str]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True

class QuestionsUpdate(BaseModel):
    question_uz: Optional[str]=None
    question_ru: Optional[str]=None
    answer_uz: Optional[str]=None
    answer_ru: Optional[str]=None
    status: Optional[int]=None
    sphere_id:Optional[int]=None
    id:int
    class Config:
        orm_mode = True



class Questions(BaseModel):
    id:int
    question_uz: Optional[str]=None
    question_ru: Optional[str]=None
    answer_uz: Optional[str]=None
    answer_ru: Optional[str]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    sphere_id:Optional[int]=None
    hrsphere:Optional[Sphere]=None
    class Config:
        orm_mode = True


class UpdateComplaint(BaseModel):
    id:int
    tel_id: Optional[str]=None
    complaint: Optional[str]=None
    status: Optional[int]=None
    deny_reason: Optional[str]=None
    category_id: Optional[int]=None 
    class Config:
        orm_mode = True



class Hrcommunication(BaseModel):
    id:int
    hrcomplaint_id:int
    text: Optional[str]=None
    status: Optional[int]=None
    url: Optional[str]=None
    user_id: Optional[int]=None
    user: Optional[User]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True

class GetHrcommunication(BaseModel):
    hrcomplaint_id:Optional[int]=None
    client_id:Optional[int]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True


class HrCategoryCreate(BaseModel):
    name: Optional[str]=None
    status: Optional[int]=1
    hrsphere_id: Optional[int]=None
    class Config:
        orm_mode = True


class HrCategory(BaseModel):
    id:int
    name: Optional[str]=None
    status: Optional[int]=None
    hrsphere_id: Optional[int]=None
    hrsphere: Optional[Sphere]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class HrCategoryUpdate(BaseModel):   
    id:int
    name: Optional[str]=None
    status:Optional[int]=None
    hrsphere_id: Optional[int]=None



class HrClients(BaseModel):
    id:int
    name: Optional[str]=None
    status: Optional[int]=None
    sphere: Optional[int]=None
    lang: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True

class Hrcomplaints(BaseModel):
    id:int
    complaint: Optional[str]=None
    sphere_id: Optional[int]=None
    hrclient_id: Optional[int]=None
    hrclient: Optional[HrClients]=None
    hrcategory: Optional[HrCategory]=None
    hrtype: Optional[int]=None
    status: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    deny_reason: Optional[str]=None
    class Config:
        orm_mode = True


#hello world