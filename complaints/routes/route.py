from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Form,UploadFile
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
import random
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
    generate_random_filename

)
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal

from dotenv import load_dotenv
import os
load_dotenv()
from complaints.queries import crud
from complaints.models import request_model
from users.schemas import user_sch
from complaints.schemas import schema


complain_router = APIRouter()



@complain_router.post("/country", summary="Create country",tags=["Complaint"],response_model=schema.Country)
async def create_country(
    form_data: schema.CreateCountry,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_country(db, form_data)

@complain_router.put("/country", summary="Update country",tags=["Complaint"],response_model=schema.Country)
async def update_country(
    form_data: schema.UpdateCountry,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_country(db, form_data)


@complain_router.get("/country", summary="Get country",tags=["Complaint"],response_model=Page[schema.Country])
async def get_country(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_country(db, id))


@complain_router.post("/category", summary="Create category",tags=["Complaint"],response_model=schema.Category)
async def create_category(
    form_data: schema.CreateCategory,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_category(db, form_data)

@complain_router.put("/category", summary="Update category",tags=["Complaint"],response_model=schema.Category)
async def update_category(
    form_data: schema.UpdateCategory,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_category(db, form_data)

@complain_router.get("/category", summary="Get category",tags=["Complaint"],response_model=Page[schema.Category])
async def get_category(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.get_category(db, id)

@complain_router.post("/sub-category", summary="Create sub-category",tags=["Complaint"],response_model=schema.SubCategory)
async def create_sub_category(
    form_data: schema.CreateSubCategory,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_subcategory(db, form_data)

@complain_router.put("/sub-category", summary="Update sub-category",tags=["Complaint"],response_model=schema.SubCategory)
async def update_sub_category(
    form_data: schema.UpdateSubCategory,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_subcategory(db, form_data)

@complain_router.get("/sub-category", summary="Get sub-category",tags=["Complaint"],response_model=Page[schema.SubCategory])
async def get_sub_category(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.get_subcategory(db, id)



@complain_router.post("/branches", summary="Create branches",tags=["Complaint"],response_model=schema.Branchs)
async def create_branch(
    form_data: schema.CreateBranch,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    query = crud.create_branch(db, form_data)
    password = generate_random_filename(length=20)+str(query.id)
    updated_password = crud.update_branch_pass(db,query.id,password=password)
    return updated_password



@complain_router.put("/branches", summary="Update branches",tags=["Complaint"],response_model=schema.Branchs)   
async def update_branch(
    form_data: schema.UpdateBranch,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_branch(db, form_data)
    if form_data.password:
        password = generate_random_filename(length=20)+str(query.id)
        updated_password = crud.update_branch_pass(db,query.id,password=password)
        return updated_password
    return query



@complain_router.get("/branches", summary="Get branches",tags=["Complaint"],response_model=Page[schema.Branchs])
async def get_branch(
    id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[int] = None,
    country_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_branch(db, id=id,name=name,status=status,country_id=country_id))








