from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from complaints.schemas.country import GetCountries


class GetBranchs(BaseModel):
    id: int
    name: Optional[str] = None
    country_id: Optional[int] = None
    country : Optional[GetCountries] = None

    class Config:
        orm_mode = True