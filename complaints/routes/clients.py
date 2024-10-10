
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
from complaints.queries.clients import get_clients

client_router = APIRouter()


@client_router.get("/clients/")
async def get_clients(
        telegram_id: int ,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get all clients
    """
    return get_clients(db=db, telegram_id=telegram_id)
