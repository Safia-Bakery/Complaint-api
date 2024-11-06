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
        status = 0,
        manager_number = form_data.manager_number
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_my_complaints(db:Session,client_id,):
    query = db.query(Complaints).filter(Complaints.client_id==client_id)
    return query.all()


def get_my_archive_complaints(db:Session,client_id):
    query = db.query(Complaints).filter(
        Complaints.client_id==client_id,
        Complaints.status.in_([2,3]),
        Complaints.updated_at > datetime.now(timezone_tash).date()
    )
    return query.all()


def get_my_result_complaints(db:Session,client_id):
    query = db.query(Complaints).filter(
        Complaints.client_id==client_id,
        Complaints.status.in_([2]),
        Complaints.updated_at <= datetime.now(timezone_tash).date()
    )
    return query.all()

def get_my_inprocess_complaints(db:Session,client_id):
    query = db.query(Complaints).filter(
        Complaints.client_id==client_id,
        Complaints.status.in_([0,1]),
    )
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

    if form_data.first_response is not None:
        query.first_response_time = datetime.now(timezone_tash)
        query.first_response = form_data.first_response
    if form_data.second_response is not None:
        query.second_response_time = datetime.now(timezone_tash)
        query.second_response = form_data.second_response
    if form_data.status is not None:
        query.status = form_data.status
    if form_data.otk_status is not None:
        if form_data.otk_status in [2,3]:
            query.status = form_data.status
        query.otk_status = form_data.otk_status

    if form_data.autonumber is not None:
        query.autonumber = form_data.autonumber
    if form_data.corrections is not None:
        query.corrections = form_data.corrections
    if form_data.deny_reason is not None:
        query.deny_reason = form_data.deny_reason

    if form_data.manager_number is not None:
        query.manager_number = form_data.manager_number
    if form_data.match_standard is not None:
        query.match_standard = form_data.match_standard
    if form_data.date_clients_complaint is not None:
        query.date_clients_complaint = form_data.date_clients_complaint



    db.commit()

    return query


def update_otk_status(db:Session,complaint_id,otk_status):
    query = db.query(Complaints).filter(Complaints.id==complaint_id).first()
    query.otk_status = otk_status
    db.commit()
    return query




