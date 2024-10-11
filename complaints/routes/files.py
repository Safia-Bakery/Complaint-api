import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from complaints.queries.iikofolders import update_create_folders
from complaints.utils.utils import file_name_generator
from services import get_db, get_current_user
from complaints.utils.api_requests import ApiRoutes
from users.schemas import user_sch

files_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


@files_router.on_event("/files/")
async def folders_job(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):

    file_path = f"files/{file_name_generator()}{file.filename}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)
    return {"file_name": file_path}


