from typing import Optional

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from services import get_db, get_current_user
from complaints.utils.api_requests import ApiRoutes
from users.schemas import user_sch
from complaints.schemas.v2complaints import V2CreateComplaints,V2ComplaintsGet
from complaints.queries import iikoproducts
from complaints.queries.v2complaints import create_complaint,get_my_complaints
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







