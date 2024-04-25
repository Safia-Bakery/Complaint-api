from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Form,UploadFile
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from datetime import datetime
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

@complain_router.get("/category", summary="Get category",tags=["Complaint"],response_model=list[schema.Category])
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
    category_id: Optional[int] = None,
    id: Optional[int] = None,
    country_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_subcategory(db=db,id=id,category_id=category_id,country_id=country_id))



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



@complain_router.post("/complaints", summary="Create complaint",tags=["Complaint"],response_model=schema.Complaints)
async def create_complaint(
    files: list[UploadFile] = None,
    product_name:Annotated[str,Form(...)]=None,
    client_name:Annotated[int,Form(...)]=None,
    client_number:Annotated[str,Form(...)]=None,
    client_gender:Annotated[str,Form(...)]=None,
    date_purchase:Annotated[datetime,Form(...)]=None,
    date_return:Annotated[datetime,Form(...)]=None,
    comment:Annotated[str,Form(...)]=None,
    autonumber:Annotated[str,Form(...)]=None,
    subcategory_id:Annotated[int,Form(...)]=None,
    branch_id:Annotated[int,Form(...)]=None,
    db: Session = Depends(get_db)):
    create_complaint = crud.create_complaint(db,product_name=product_name,
                                 branch_id=branch_id,
                                 subcategory_id=subcategory_id,
                                 client_name=client_name,
                                 client_number=client_number,
                                 client_gender=client_gender,
                                 date_purchase=date_purchase,
                                 date_return=date_return,
                                 comment=comment,
                                 autonumber=autonumber)
    if files:
        for file in files:
            file_path = f"files/{generate_random_filename()}{file.filename}"
            
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)

            crud.create_file(db=db,complaint_id=create_complaint.id,file_path=file_path)
    return create_complaint

@complain_router.put("/complaints", summary="Update complaint",tags=["Complaint"],response_model=schema.Complaints)
async def update_complaint(
    form_data: schema.UpdateComplaint,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_complaints(db, form_data)


@complain_router.get("/complaints", summary="Get complaint",tags=["Complaint"],response_model=Page[schema.Complaints])
async def get_complaints(
    id: Optional[int] = None,
    subcategory_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    status: Optional[int] = None,
    otk_status: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_complaints(db=db,id=id,subcategory_id=subcategory_id,branch_id=branch_id,otk_status=otk_status,status=status))










