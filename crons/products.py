import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter
from sqlalchemy.orm import Session

from complaints.queries.iikoproducts import update_create_products
from services import get_db
from microservice.api_requests import ApiRoutes


folder_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


api_route = ApiRoutes()


def products_job(db: Session):
    products_list = api_route.get_all_products()
    update_create_products(db, products_list)

    return True


@folder_cron_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=13, minute=33, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(products_job, trigger=trigger, args=[next(get_db())])
    scheduler.start()

