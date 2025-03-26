import os
import threading
import time
from contextlib import contextmanager, asynccontextmanager
from typing import Optional
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from database import SessionLocal
from hrcomplaint.queries.notifications import add_notification, edit_notification, get_notifications, \
    remove_notification
from hrcomplaint.schemas.notifications import CreateNotification, UpdateNotification
from hrcomplaint.queries.hr_crud import get_hr_clients
from hrcomplaint.schemas.notifications import Notification
from services import get_db, get_current_user, send_textmessage_telegram
from users.schemas import user_sch


BOTTOKEN = os.environ.get('BOT_TOKEN_HR')
SCHEDULER_DATABASE_URL = os.environ.get('SCHEDULER_DATABASE_URL')


notification_router = APIRouter()


jobstores = {
    "default": SQLAlchemyJobStore(url=SCHEDULER_DATABASE_URL)
}
scheduler = BackgroundScheduler(jobstores=jobstores)

if not scheduler.running:
    print("🚀 Starting scheduler...")
    scheduler.start()  # ✅ Start only once


scheduler_lock = threading.Lock()




def get_scheduler():
    return scheduler



@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def send_scheduled_notification(bot_token, chat_ids, message_text, notification_id):
    for i, chat_id in enumerate(chat_ids):
        if i % 10 == 0:
            # print(f"Sleeping before sending {i}-th client ...")
            time.sleep(3)

        send_textmessage_telegram(bot_token=bot_token, chat_id=chat_id, message_text=message_text)

    if notification_id is not None:
        with get_session() as session:
            edit_notification(db=session, id=notification_id, status=1)



@notification_router.get("/notification", summary="Get scheduled notifications", tags=["Notifications"],
                         response_model=Page[Notification])
async def get_notification_list(
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    # print("scheduled jobs: ", scheduler.get_jobs())
    notifications = get_notifications(db=db)
    return paginate(notifications)


@notification_router.get("/notification/{id}", summary="Get scheduled notification", tags=["Notifications"],
                         response_model=Notification)
async def get_notification(
        id: int,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    notification = get_notifications(db=db, id=id)
    if notification is None:
        raise HTTPException(status_code=404, detail=f"There is no any notification with id №{id}")
    return notification


@notification_router.post("/notification", summary="Create scheduled notifications", tags=["Notifications"],
                          response_model=Notification)
async def create_notification(
        form_data: CreateNotification,
        job_scheduler: BackgroundScheduler = Depends(get_scheduler),
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    created_notification = add_notification(db=db, form_data=form_data, user_id=current_user.id)
    notification_id = created_notification.id
    users = get_hr_clients(db=db, spheres=form_data.receivers_sphere)
    chat_ids = [user.id for user in users]
    # chat_ids = [1618364630, 1950245915]
    # print("job_scheduler: ", job_scheduler)
    try:
        job_scheduler.add_job(
            send_scheduled_notification,
            "date",
            run_date=form_data.scheduled_at,
            args=[BOTTOKEN, chat_ids, created_notification.text, notification_id],
            id=str(notification_id)
        )
        # print("Jobs: ", job_scheduler.get_jobs())
    except ConflictingIdError:
        print(f"Job '{notification_id}' already exists!")

    return created_notification



@notification_router.put("/notification", summary="Update scheduled notifications", tags=["Notifications"],
                         response_model=Notification)
async def update_notification(
        form_data: UpdateNotification,
        job_scheduler: BackgroundScheduler = Depends(get_scheduler),
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    notification_id = None  # Declare it before locking to prevent issues

    with scheduler_lock:
        updated_notification = edit_notification(db=db, form_data=form_data)
        if updated_notification is None:
            raise HTTPException(status_code=404, detail=f"This notification with id №{form_data.id} has been already executed !")
        notification_id = updated_notification.id
        users = get_hr_clients(db=db, spheres=form_data.receivers_sphere)
        chat_ids = [user.id for user in users]
        # chat_ids = [1618364630, 1950245915]
        try:
            job_scheduler.modify_job(
                job_id=str(notification_id),
                args=[BOTTOKEN, chat_ids, updated_notification.text, None]
            )
            if form_data.scheduled_at is not None:
                job_scheduler.reschedule_job(job_id=str(notification_id), trigger=DateTrigger(run_date=form_data.scheduled_at))
            # print("Jobs: ", job_scheduler.get_jobs())
        except JobLookupError:
            print(f"'{notification_id}' job not found or already has completed !")

    return updated_notification



@notification_router.delete("/notification", summary="Delete scheduled notifications", tags=["Notifications"])
async def delete_notification(
        id: int,
        job_scheduler: BackgroundScheduler = Depends(get_scheduler),
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    deleted_notification = remove_notification(db=db, id=id)
    notification_id = deleted_notification.id
    try:
        job_scheduler.remove_job(
            job_id=str(notification_id)
        )
    except JobLookupError:
        print(f"'{notification_id}' job not found or already has completed !")

    return {"Message": f"Notification №{notification_id} was deleted successfully !"}

