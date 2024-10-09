import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter
from sqlalchemy.orm import Session

from complaints.queries.iikofolders import update_create_folders
from services import get_db
from complaints.utils.api_requests import ApiRoutes


folder_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')




def folders_job(db: Session):
    api_route = ApiRoutes()
    folder_list = api_route.get_all_folders()
    update_create_folders(db, folder_list)

    return True


@folder_cron_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=17, minute=34 , second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(folders_job, trigger=trigger, args=[next(get_db())])
    scheduler.start()

