from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from complaints.models import request_model as model


def get_client(db:Session,id: Optional[int] = None):
    query = db.query(model.Clients)
    if id is not None:
        query = query.filter(model.Clients.id == id)
    return query.first()



def create_client(db:Session,name,id,branch_id):
    query = model.Clients(
        id=id,
        name=name,
        branch_id=branch_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_client(db:Session,id,branch_id):
    query = db.query(model.Clients).filter(model.Clients.id==id).first()
    if query:
        query.branch_id=branch_id
        db.commit()
        db.refresh(query)
    return query

def get_branchs(db:Session,password:Optional[int]=None,id:Optional[int]=None):
    query = db.query(model.Branchs)
    if password is not None:
        query = query.filter(model.Branchs.password==password)
    if id is not None:
        query = query.filter(model.Branchs.id==id)
        
    return query.first()


def get_category(db:Session,name: Optional[str] = None):
    query = db.query(model.Categories)
    if name is not None:
        query = query.filter(model.Categories.name.ilike(f"%{name}%"))
    return query.all()


def get_subcategory(db:Session,name: Optional[str] = None,category_id: Optional[int] = None):
    query = db.query(model.Subcategories).filter(model.Subcategories.category_id==category_id)
    if name is not None:
        query = query.filter(model.Subcategories.name.ilike(f"%{name}%"))
    return query.all()



def create_complaint(db:Session,branch_id,subcategory_id,name, phone_number,comment,date_purchase,datereturn):
    query = model.Complaints(
        branch_id=branch_id,
        subcategory_id=subcategory_id,
        client_name=name,
        client_number=phone_number,
        comment=comment,
        date_purchase=date_purchase,
        date_return=datereturn,
        is_client=False,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_file(db:Session,complaint_id,file_name):
    query = model.Files(
        complaint_id=complaint_id,
        url=file_name
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



