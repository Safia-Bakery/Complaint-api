
from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class GetFiles(BaseModel):
    id :Optional[int] = None
    url : Optional[str] = None

    class Config:
        orm_mode = True
