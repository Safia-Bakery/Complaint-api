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
    generate_random_filename,
    send_file_telegram,
    send_textmessage_telegram
)

from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal

from dotenv import load_dotenv
import os
load_dotenv()
from hrcomplaint.queries import hr_crud
from hrcomplaint.schemas import hr_schema
from users.schemas import user_sch

BOTTOKEN = os.environ.get('BOT_TOKEN_HR')
hr_router = APIRouter()

@hr_router.post("/hr/sphere", summary="Create sphere",tags=["HR"],response_model=hr_schema.Sphere) 
async def create_sphere(
    form_data: hr_schema.SphereCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return hr_crud.create_sphere(db, form_data)


@hr_router.get("/hr/sphere", summary="Get sphere",tags=["HR"],response_model=list[hr_schema.Sphere])
async def get_sphere(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return hr_crud.get_sphere(db, id)




@hr_router.post("/hr/questions", summary="Create questions",tags=["HR"],response_model=hr_schema.Questions)
async def create_questions(
    form_data: hr_schema.QuestionsCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return hr_crud.create_questions(db, form_data)

@hr_router.put("/hr/questions", summary="Update questions",tags=["HR"],response_model=hr_schema.Questions)
async def update_questions(
    form_data: hr_schema.QuestionsUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return hr_crud.update_questions(db, form_data)


@hr_router.get("/hr/questions", summary="Get questions",tags=["HR"],response_model=Page[hr_schema.Questions])
async def get_questions(
    id: Optional[int] = None,
    sphere_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(hr_crud.get_questions(db, id,sphere_id))



@hr_router.get('/hr/complaints',summary="Get complaint",tags=["HR"],response_model=Page[hr_schema.Hrcomplaints])
async def get_complaints(
    id: Optional[int] = None,
    hrtype: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(hr_crud.get_complaints(db, id,hrtype))

@hr_router.put('/hr/complaints',summary="update complaint",tags=["HR"])
async def update_complaint(
    form_data: hr_schema.UpdateComplaint,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return hr_crud.update_complaint(db, form_data)






@hr_router.get('/hr/communictation',summary="Get messages",tags=["HR"],response_model=Page[hr_schema.Hrcommunication])
async def get_communication(
    hrcomplaint_id: Optional[int] = None,
    hrclient_id: Optional[int] = None,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    if hrcomplaint_id is None and hrclient_id is None:
        raise HTTPException(status_code=400, detail="hrcomplaint_id or user_id is required")
    return paginate(hr_crud.get_communication(db, status=status,hrcomplaint_id=hrcomplaint_id,hrclient_id=hrclient_id))

@hr_router.get('/hr/clients',summary="Get clients",tags=["HR"],response_model=Page[hr_schema.HrClients])
async def get_clients(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(hr_crud.get_hrclients(db, id))


@hr_router.post('/hr/communictation',summary="Create message",tags=["HR"])  
async def create_communication(
    text:Annotated[str,Form()]= None,
    hrcomplaint_id:Annotated[int,Form()]= None,
    file:UploadFile=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    if text is None and file is None:
        raise HTTPException(status_code=400, detail="Text or file is required")
    if file:
        file_path = f"files/{generate_random_filename}{file.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None
    query = hr_crud.create_communication(db, text=text, hrcomplaint_id=hrcomplaint_id, user_id=current_user.id,url=file_path)
    if file is not None:
        send_file_telegram(bot_token=BOTTOKEN,chat_id=query.hrcomplaint.hrclient_id,file_path=file_path)
    if text is not None:
        send_textmessage_telegram(bot_token=BOTTOKEN,chat_id=query.hrcomplaint.hrclient_id,message_text=text)
    return query





