from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class GetHastStamRoles(BaseModel):
    id:int
    name: Optional[str]=None
    status: int



class GetStampUsers(BaseModel):
    id:int
    username:str
    name:Optional[str]=None
    role : Optional[GetHastStamRoles]=None
    class Config:
        orm_mode = True
