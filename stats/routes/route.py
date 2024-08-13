from fastapi import APIRouter
from typing import TypeVar
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
    generate_random_filename,
    send_file_telegram,
    send_textmessage_telegram

)
from fastapi_pagination.customization import CustomizedPage,UseParamsFields
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal

from dotenv import load_dotenv
import os
load_dotenv()
from complaints.models import request_model
from hrcomplaint.models import hr_model
from users.models import user_model
import pytz
from users.schemas import user_sch
from complaints.schemas import schema
from datetime import date

BOT_TOKEN_HR = os.getenv("BOT_TOKEN_HR")
BOT_TOKEN_COMPLAINT = os.getenv("BOT_TOKEN_COMPLAINT")

timezonetash = pytz.timezone("Asia/Tashkent")
from stats.queries import query



stats_router = APIRouter()



@stats_router.get("/stats", summary="Create stats", )
async def create_stats(
        from_date:date,
        to_date:date,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    general_stats = {}
    general_stats["workers_comparison"] = query.get_workers_comparison_stats(db)
    general_stats["complaint_service"] = query.get_complaint_service_stats(db)
    general_stats["complaint_quality"] = query.get_complaint_quality_stats(db)
    general_stats['qrcode_stats'] = query.get_qr_client_stats(db)
    general_stats['with_categories'] = query.get_subcategories_stats(db,from_date,to_date)
    general_stats['monthly_stats'] = query.last_6_monthly_complaint_stats(db)
    general_stats['country_stats'] = query.get_complaint_according_country_expenditure_stats(db, from_date, to_date)
    return general_stats



@stats_router.get("/stats/hr", summary="Create stats", )
async def create_stats(
        from_date:date,
        to_date:date,
        sphere_id:int,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):

    general_stats = {}
    general_stats["with_categories"] = query.get_hr_complaint_categories_stats(db,from_date,to_date,sphere_id)
    general_stats["complaint_count"] = query.get_hr_complaint_total_number_stats(db,from_date,to_date,sphere_id)
    general_stats["question_count"] = query.get_hr_question_total_number_stats(db,from_date,to_date,sphere_id)
    general_stats["advice_count"] = query.get_hr_advice_total_number_stats(db,from_date,to_date,sphere_id)





    return general_stats


