
from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas.v2role import GetStampUsers


class CreateComplaintStampers(BaseModel):
    complaint_id: int
    user_id: int
    user : Optional[GetStampUsers] = None
    class Config:
        orm_mode = True


class DeleteComplaintStampers(BaseModel):
    complaint_id: int
    user_id: int
    class Config:
        orm_mode = True


class GetComplaintStampers(BaseModel):
    id :Optional[int] = None
    complaint_id : Optional[int] = None
    user_id : Optional[int] = None
    user : Optional[GetStampUsers] = None

    class Config:
        orm_mode = True