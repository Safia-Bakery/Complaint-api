from typing import Optional

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from services import get_db, get_current_user, send_file_telegram, send_textmessage_telegram
from complaints.utils.api_requests import ApiRoutes
from users.schemas import user_sch
from complaints.schemas.v2complaints import V2CreateComplaints,V2ComplaintsGet,V2GetOneComplaint,V2UpdateComplaints
from complaints.queries import iikoproducts
from complaints.queries.v2complaints import create_complaint,get_my_complaints,get_one_complaint,update_complaint,update_otk_status
from complaints.queries.complaint_product import create_complaint_product
from complaints.queries.files import create_file




v2_complaints_router = APIRouter()



@v2_complaints_router.post("/complaints/", response_model=V2ComplaintsGet)
async def create_complaints(
        form_data: V2CreateComplaints,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Create new complaint
    """
    complaint_created = create_complaint(db=db, form_data=form_data)
    if form_data.products is not None:
        for product in form_data.products:
            create_complaint_product(db=db, complaint_id=complaint_created.id, product_id=product)

    if form_data.files is not None:
        for file in form_data.files:
            create_file(db=db, complaint_id=complaint_created.id, url=file)
    return complaint_created



@v2_complaints_router.get("/complaints/my/", response_model=Page[V2ComplaintsGet])
async def get_complaints_function(
        client_id:Optional[int]=None,
        status : Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get all complaints
    """
    return paginate(get_my_complaints(db=db, client_id=client_id, status=status))



@v2_complaints_router.get("/complaints/{complaint_id}/", response_model=V2GetOneComplaint)
async def get_one_complaint_api(
        complaint_id: int,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get one complaint
    """
    return get_one_complaint(db=db, complaint_id=complaint_id)



@v2_complaints_router.put("/complaints/", response_model=V2GetOneComplaint)
async def update_complaint_api(
        form_data: V2UpdateComplaints,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user),
):
    """
    Update complaint
    """
    query =update_complaint(db=db, complaint_id=form_data.id, form_data=form_data)
    service_id = query.subcategory.country.service_id
    quality_id = query.subcategory.country.quality_id
    if form_data.status == 1:
        text_to_send = f"""
    📁{query.subcategory.category.name}
    🔘Категория: {query.subcategory.name}
    🧑‍💼Имя: {query.client_name}
    📍Филиал: {query.branch.name}
    🕘Дата покупки: {query.date_purchase}
    🚛Дата отправки: {query.date_return}\n
    💬Комментарии: {query.comment}
                """
        if not query.file:
            if query.subcategory.category_id == 1:
                send_textmessage_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id, message_text=text_to_send)
            else:
                send_textmessage_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id, message_text=text_to_send)
        else:

            if query.subcategory.category_id == 1:
                message_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id,
                                                    file_path=None, caption=text_to_send)

                for i in query.file:
                    file_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id, file_path=i.url,
                                                     caption=None,
                                                     reply_to_message_id=message_sended['result']['message_id'])
            else:
                message_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id,
                                                    file_path=None, caption=text_to_send)
                for i in query.file:
                    file_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id, file_path=i.url,
                                                     caption=None,
                                                     reply_to_message_id=message_sended['result']['message_id'])

    if form_data.status == 1 and query.subcategory.category_id in [1, 5]:
        update_otk_status(db=db, complaint_id=query.id, otk_status=1)

    # if status is one send message to channel
    # if complaint category_id is equal to one thend send message to quality group
    # if complaint category_id is equal to 2 then send message to service group

    return query











