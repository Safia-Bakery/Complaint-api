
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
from complaints.queries.clients import get_clients as get_clients_query
from complaints.schemas.clients import GetClients
from complaints.queries.branchs import get_branchs


client_router = APIRouter()


@client_router.get("/clients/", response_model=GetClients)
async def get_clients(
        telegram_id: int ,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get all clients
    """
    query = get_clients_query(db=db, telegram_id=telegram_id)
    branch = get_branchs(db=db, id=query.branch_id)
    query.branch = branch
    return query