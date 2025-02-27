from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from hrcomplaint.models import hr_model
from hrcomplaint.schemas.notifications import CreateNotification, UpdateNotification


def add_notification(db: Session, form_data: CreateNotification, user_id):
    query = hr_model.Notifications(
        text=form_data.text,
        created_by=user_id,
        scheduled_at=form_data.scheduled_at,
        receivers_sphere=form_data.receivers_sphere
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def edit_notification(db: Session, form_data: Optional[UpdateNotification] = None, id: Optional[int] = None, status: Optional[int] = None):
    if form_data is not None:
        query = db.query(hr_model.Notifications).get(ident=form_data.id)
        if form_data.text is not None:
            query.text = form_data.text
        if form_data.scheduled_at is not None:
            query.scheduled_at = form_data.scheduled_at
        if form_data.receivers_sphere is not None:
            query.receivers_sphere = form_data.receivers_sphere
    else:
        query = db.query(hr_model.Notifications).get(ident=id)
        if status is not None:
            query.status = status

    db.commit()
    db.refresh(query)
    return query



def get_notifications(db: Session, id: Optional[int] = None):
    query = db.query(hr_model.Notifications)
    if id is not None:
        query = query.get(ident=id)
        if not query:
            return None
        return query

    query = query.order_by(desc(hr_model.Notifications.id)).all()
    return query


def remove_notification(db: Session, id):
    query = db.query(hr_model.Notifications).get(ident=id)
    db.delete(query)
    db.commit()
    return query