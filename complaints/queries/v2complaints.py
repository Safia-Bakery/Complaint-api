from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from complaints.models import request_model
from complaints.schemas.v2complaints import V2CreateComplaints
from complaints.models.request_model import Complaints


def create_complaint(db:Session,form_data:V2CreateComplaints):
    query = Complaints(
        product_name=form_data.product_name,
        client_name=form_data.client_name,
        client_number=form_data.client_number,
        date_purchase=form_data.date_purchase,
        date_return=form_data.date_return,
        comment=form_data.comment,
        subcategory_id=form_data.subcategory_id,
        branch_id=form_data.branch_id,
        expense=form_data.expense,
        client_id=form_data.client_id,
        status = 0
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_my_complaints(db:Session,client_id,status):
    query = db.query(Complaints).filter(Complaints.client_id==client_id)
    if status is not None:
        query = query.filter(Complaints.status==status)
    return query.all()


