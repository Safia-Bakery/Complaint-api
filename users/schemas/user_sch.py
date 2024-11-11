from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID

class Actions(BaseModel):
    id:int
    name: Optional[str]=None
    status: int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None



class Pages(BaseModel):
    id:int
    name: Optional[str]=None
    status: int
    action: list[Actions]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None




class Permissions(BaseModel):
    id:int
    action_id:int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    status: int
    class Config:
        orm_mode = True

class Roles(BaseModel):
    id:int
    name: Optional[str]=None
    status: int
    permission: list[Permissions]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True

    





class User(BaseModel):
    id:int
    name: Optional[str]=None
    username: Optional[str]=None
    phone_number: Optional[str]=None
    status: int
    role_id: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    permissions: Optional[dict]={}
    class Config:
        orm_mode = True



class Users(BaseModel):
    id:int
    name: Optional[str]=None
    username: Optional[str]=None
    phone_number: Optional[str]=None
    status: int
    role_id: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    role: Optional[Roles]=None
    stamp   : Optional[str]=None
    telegram_id: Optional[str]=None
    signature: Optional[str]=None
    class Config:
        orm_mode = True






class UserCreate(BaseModel):
    username:str
    password:str
    name: Optional[str]=None
    role_id:Optional[int]=None
    phone_number: Optional[str]=None,
    status:Optional[int]=1
    telegram_id: Optional[str]=None
    

class UserUpdate(BaseModel):
    #username:Optional[str]=None
    password:Optional[str]=None
    name: Optional[str]=None
    phone_number: Optional[str]=None
    id:int
    role_id:Optional[int]=None
    status:Optional[int]=None
    stamp : Optional[str]=None
    telegram_id: Optional[str]=None
    signature: Optional[str]=None




class ResetPassword(BaseModel):
    password:str
    phone_number:Optional[str]=None 


class RoleCreate(BaseModel):
    name:str
    status:Optional[int]=1
    has_stamp: Optional[str]=None





class PermissionsGet(BaseModel):
    id:int
    action_id:int
    action:Actions
    role_id:int
    status:int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class RoleGet(BaseModel):
    id:int
    name:str
    permission: list[PermissionsGet]=None
    status:int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[int]=None
    permissions:Optional[list[int]]=None
