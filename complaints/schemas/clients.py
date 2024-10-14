from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from complaints.schemas.branchs import GetBranchs


class GetClients(BaseModel):
    id: int
    status: Optional[int] = None
    name: Optional[str] = None
    branch : Optional[GetBranchs] = None

    class Config:
        orm_mode = True