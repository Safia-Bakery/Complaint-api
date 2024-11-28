import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from complaints.queries.iikofolders import update_create_folders
from complaints.utils.utils import file_name_generator
from services import get_db, get_current_user
from complaints.utils.api_requests import ApiRoutes
from complaints.utils.utils import sendtotelegram_inline_buttons
from users.schemas import user_sch
from complaints.core.config import BOT_TOKEN_COMPLAINT
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
    query = create_complaint_stampers(db=db, complaint_id=form_data.complaint_id, user_id=form_data.user_id)

    message_text = f"""Заявка: №{form_data.complaint_id}
Филиал: {query.complaint.branch.name}
Качество: {query.complaint.subcategory.category.name}
Категория: {query.complaint.subcategory.name}
Комментарии: {query.complaint.comment}
Дата поступления: {query.complaint.created_at.strftime("%d.%m.%Y %H:%M")} \n\n
Заключение: {query.complaint.second_response}
"""
    sendtotelegram_inline_buttons(BOT_TOKEN_COMPLAINT, query.user.telegram_id, message_text )


    return query


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




