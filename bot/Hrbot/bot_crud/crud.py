from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from database import  SessionLocal
from hrcomplaint.models import hr_model




def get_user(id: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(hr_model.Hrclients)
        if id is not None:
            query = query.filter(hr_model.Hrclients.id == id)
        return query.first()


def create_user(name,lang,sphere,id):
    with SessionLocal() as db:
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


def get_questions(name: Optional[str] = None,sphere: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(hr_model.Hrquestions)
        if name is not None:
            query = query.filter(or_(hr_model.Hrquestions.question_ru.ilike(f"%{name}%"),hr_model.Hrquestions.question_uz.ilike(f"%{name}%")))
        if sphere is not None:
            query = query.filter(hr_model.Hrquestions.sphere_id==sphere)
        return query.all()


def update_user(id:Optional[int]=None,lang:Optional[int]=None,sphere:Optional[int]=None):
    with SessionLocal() as db:
        query = db.query(hr_model.Hrclients).filter(hr_model.Hrclients.id==id).first()
        if lang is not None:
            query.lang = lang
        if sphere is not None:
            query.sphere = sphere
        db.commit()
        db.refresh(query)
        return query





def get_spheres(name: Optional[str] = None):
    with SessionLocal() as db:
        query = db.query(hr_model.Hrspheras)
        if name is not None:
            query = query.filter(hr_model.Hrspheras.name.ilike(f"%{name}%"))
        return query.all()


def create_complaint(tel_id,complaint,sphere_id,hrtype,category):
    with SessionLocal() as db:
        query = hr_model.Hrcomplaints(
            complaint=complaint,
            sphere_id=sphere_id,
            hrclient_id=tel_id,
            status=0,
            hrtype=hrtype,
            category_id=category

        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query


def create_message(hrcomplaint_id,url,text):
    with SessionLocal() as db:
        query = hr_model.Hrcommunications(
            hrcomplaint_id=hrcomplaint_id,
            text=text,
            url=url
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query

def get_complaints(id: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(hr_model.Hrcomplaints)
        if id is not None:
            query = query.filter(hr_model.Hrcomplaints.hrclient_id==id)
        return query.order_by(hr_model.Hrcomplaints.created_at.desc()).all()


def get_categories(id: Optional[int] = None,name: Optional[str] = None,hrsphere_id: Optional[int] = None):
    with SessionLocal() as db:
        query = db.query(hr_model.HrCategories).filter(hr_model.HrCategories.status==1)
        if id is not None:
            query = query.filter(hr_model.HrCategories.id == id)
        if name is not None:
            query = query.filter(hr_model.HrCategories.name.ilike(f"%{name}%"))
        if hrsphere_id is not None:
            query = query.filter(hr_model.HrCategories.hrsphere_id==hrsphere_id)
        return query.all()
