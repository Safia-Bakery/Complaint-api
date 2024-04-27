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



def create_client(db:Session,name,id):
    query = model.Clients(
        id=id,
        name=name
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_branchs(db:Session,password):
    query = db.query(model.Branchs).filter(model.Branchs.password==password)
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