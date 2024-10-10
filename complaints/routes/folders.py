import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from services import get_db, get_current_user
from complaints.utils.api_requests import ApiRoutes
from complaints.schemas import schema
from users.schemas import user_sch
from typing import Optional
from complaints.queries import iikofolders
from complaints.queries.iikoproducts import get_iiko_products_by_parent_id
from uuid import UUID


folder_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


@folder_cron_router.get("/folders/search/", summary="Search folders", tags=["Folders"])
async def get_searched_folders(
        name: Optional[str] =None,
        parent_id : Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    folders_result = iikofolders.get_found_folders(db=db, name=name, parent_id=parent_id)
    if name is not None or parent_id is not None:
        products_result = get_iiko_products_by_parent_id(db=db, parent_id=parent_id, name=name)
    else:
        products_result = []

    results = {
        "folders": folders_result,
        "products": products_result
    }

    return results


def folders_job(db: Session):
    api_route = ApiRoutes()
    folder_list = api_route.get_all_folders()
    iikofolders.update_create_folders(db, folder_list)

    return True


@folder_cron_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=17, minute=34, second=00, timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(folders_job, trigger=trigger, args=[next(get_db())])
    scheduler.start()

