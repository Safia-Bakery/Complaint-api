import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from services import get_db, get_current_user
from complaints.utils.api_requests import ApiRoutes
from users.schemas import user_sch
from complaints.schemas import schema
from complaints.queries import iikoproducts


product_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


def products_job(db: Session):
    api_route = ApiRoutes()
    products_list = api_route.get_all_products()
    iikoproducts.update_create_products(db, products_list)
    return True


@product_cron_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=15, minute=00, second=00, timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(products_job, trigger=trigger, args=[next(get_db())])
    scheduler.start()



