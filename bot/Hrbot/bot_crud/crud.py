from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from hrcomplaint.models import hr_model


def get_user(db: Session, id: Optional[int] = None):
    query = db.query(hr_model.Hrclients)
    if id is not None:
        query = query.filter(hr_model.Hrclients.id == id)
    return query.first()


def create_user(db:Session,name,lang,sphere,id):
    query = hr_model.Hrclients(
        id=id,
        name=name,
        lang=lang,
        sphere=sphere
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_questions(db:Session,name: Optional[str] = None,sphere: Optional[int] = None):
    query = db.query(hr_model.Hrquestions)
    if name is not None:
        query = query.filter(or_(hr_model.Hrquestions.question_ru.ilike(f"%{name}%"),hr_model.Hrquestions.question_uz.ilike(f"%{name}%")))
    if sphere is not None:
        query = query.filter(hr_model.Hrquestions.sphere_id==sphere)
    return query.all()


def update_user(db:Session,id:Optional[int]=None,lang:Optional[int]=None,sphere:Optional[int]=None):
    query = db.query(hr_model.Hrclients).filter(hr_model.Hrclients.id==id).first()
    if lang is not None:
        query.lang = lang
    if sphere is not None:
        query.sphere = sphere
    db.commit()
    db.refresh(query)
    return query





def get_spheres(db:Session,name: Optional[str] = None):
    query = db.query(hr_model.Hrspheras)
    if name is not None:
        query = query.filter(hr_model.Hrspheras.name.ilike(f"%{name}%"))
    return query.all()


def create_complaint(db:Session,tel_id,complaint,sphere_id,hrtype):
    query = hr_model.Hrcomplaints(
        complaint=complaint,
        sphere_id=sphere_id,
        hrclient_id=tel_id, 
        status=0,
        hrtype=hrtype
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_message(db:Session,hrcomplaint_id,url,text):
    query = hr_model.Hrcommunications(
        hrcomplaint_id=hrcomplaint_id,
        text=text,
        url=url
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_complaints(db:Session,id: Optional[int] = None):
    query = db.query(hr_model.Hrcomplaints)
    if id is not None:
        query = query.filter(hr_model.Hrcomplaints.hrclient_id==id)
    return query.order_by(hr_model.Hrcomplaints.created_at.desc()).all()

