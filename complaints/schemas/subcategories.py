from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from complaints.schemas.categories import GetCategories


class GetSubCategories(BaseModel):
    id: int
    name: Optional[str] = None
    category_id: Optional[int] = None
    category : Optional[GetCategories] = None
    class Config:
        orm_mode = True