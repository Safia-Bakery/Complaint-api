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


folder_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


@folder_cron_router.get("/folders", summary="Get parent folders", tags=["Folders"], response_model=Page[schema.Folder])
async def get_parent_folders(db: Session = Depends(get_db), current_user: user_sch.User = Depends(get_current_user)):

    return paginate(iikofolders.get_parent_folders(db))


@folder_cron_router.get("/folders/{id}", summary="Get child folders", tags=["Folders"], response_model=Page[schema.Folder])
async def get_child_folders(id: int, db: Session = Depends(get_db), current_user: user_sch.User = Depends(get_current_user)):

    return paginate(iikofolders.get_child_folders(db=db, id=id)),


@folder_cron_router.get("/search/folders", summary="Search folders", tags=["Folders"], response_model=schema.Folder)
async def get_searched_folders(q: str = Query(None, description="Search folder"), db: Session = Depends(get_db),
                               current_user: user_sch.User = Depends(get_current_user)):
    results = iikofolders.get_found_folders(db=db, q=q)
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

