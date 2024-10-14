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
from complaints.schemas.complaint_stampers import CreateComplaintStampers,GetComplaintStampers,DeleteComplaintStampers
from complaints.queries.complaint_stampers import create_complaint_stampers,delete_complaint_stampers

stamp_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


@stamp_router.post("/complaints/stampers/", response_model=GetComplaintStampers)
async def create_complaint_stampers_api(
        form_data: CreateComplaintStampers,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Create new complaint
    """

    return create_complaint_stampers(db=db, complaint_id=form_data.complaint_id, user_id=form_data.user_id)


@stamp_router.delete("/complaints/stampers/", )
async def delete_complaint_stampers_api(
        form_data: DeleteComplaintStampers,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Delete complaint
    """
    query = delete_complaint_stampers(db=db, complaint_id=form_data.complaint_id, user_id=form_data.user_id)
    return {"status": "success", "message": query}




