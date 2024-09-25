from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from complaints.models import request_model as model

from database import SessionLocal, Base


def get_client(id: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(model.Clients)
        if id is not None:
            query = query.filter(model.Clients.id == id)
        return query.first()



def create_client(name,id,branch_id):
    with SessionLocal() as db:
        query = model.Clients(
            id=id,
            name=name,
            branch_id=branch_id
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query

def update_client(id,branch_id):
    with SessionLocal() as db:
        query = db.query(model.Clients).filter(model.Clients.id==id).first()
        if query:
            query.branch_id=branch_id
            db.commit()
            db.refresh(query)
        return query

def get_branchs(password:Optional[int]=None,id:Optional[int]=None):
    with SessionLocal() as db:
        query = db.query(model.Branchs)
        if password is not None:
            query = query.filter(model.Branchs.password==password)
        if id is not None:
            query = query.filter(model.Branchs.id==id)

        return query.first()


def get_category(name: Optional[str] = None):
    db = SessionLocal()
    query = db.query(model.Categories).filter(model.Categories.status==1)
    if name is not None:
        query = query.filter(model.Categories.name.ilike(f"%{name}%"))
    return query.all()


def get_subcategory(name: Optional[str] = None,category_id: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(model.Subcategories).filter(model.Subcategories.category_id==int(category_id))
        if name is not None:
            query = query.filter(model.Subcategories.name.ilike(f"%{name}%"))
        return query.all()



def create_complaint(branch_id,subcategory_id,name, phone_number,comment,date_purchase,datereturn,product_name):
    db = SessionLocal()

    query = model.Complaints(
        branch_id=branch_id,
        subcategory_id=subcategory_id,
        client_name=name,
        client_number=phone_number,
        comment=comment,
        date_purchase=date_purchase,
        date_return=datereturn,
        is_client=False,
        is_internal=1,
        status=0,
        product_name=product_name
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_file(complaint_id,file_name):
    with SessionLocal() as db:
        query = model.Files(
            complaint_id=complaint_id,
            url=file_name
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query








