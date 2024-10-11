from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from complaints.models import request_model
from complaints.schemas.v2complaints import V2CreateComplaints,V2UpdateComplaints
from complaints.models.request_model import Complaints

timezone_tash = pytz.timezone('Asia/Tashkent')

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


def get_one_complaint(db:Session,complaint_id):
    query = db.query(Complaints).filter(Complaints.id==complaint_id).first()
    return query



def update_complaint(db:Session,complaint_id,form_data:V2UpdateComplaints):
    query = db.query(Complaints).filter(Complaints.id==complaint_id).first()
    if form_data.product_name is not None:
        query.product_name = form_data.product_name
    if form_data.client_name is not None:
        query.client_name = form_data.client_name
    if form_data.client_number is not None:
        query.client_number = form_data.client_number
    if form_data.date_purchase is not None:
        query.date_purchase = form_data.date_purchase
    if form_data.date_return is not None:
        query.date_return = form_data.date_return
    if form_data.comment is not None:
        query.comment = form_data.comment
    if form_data.subcategory_id is not None:
        query.subcategory_id = form_data.subcategory_id
    if form_data.branch_id is not None:
        query.branch_id = form_data.branch_id
    if form_data.expense is not None:
        query.expense = form_data.expense
    if form_data.client_id is not None:
        query.client_id = form_data.client_id
    if form_data.first_response is not None:
        query.first_response_time = datetime.now(timezone_tash)
        query.first_response = form_data.first_response
    if form_data.second_response is not None:
        query.second_response_time = datetime.now(timezone_tash)
        query.second_response = form_data.second_response
    db.commit()

    return query


def update_otk_status(db:Session,complaint_id,otk_status):
    query = db.query(Complaints).filter(Complaints.id==complaint_id).first()
    query.otk_status = otk_status
    db.commit()
    return query



