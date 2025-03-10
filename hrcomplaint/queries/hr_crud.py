from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from hrcomplaint.models import hr_model
from hrcomplaint.schemas import hr_schema


def create_questions(db: Session, form_data: hr_schema.QuestionsCreate):
    db_question = hr_model.Hrquestions(
        question_uz=form_data.question_uz,
        question_ru=form_data.question_ru,
        answer_uz=form_data.answer_uz,
        answer_ru=form_data.answer_ru,
        status=form_data.status,
        sphere_id=form_data.sphere_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_questions(db: Session, form_data: hr_schema.QuestionsUpdate):
    db_question = db.query(hr_model.Hrquestions).filter(hr_model.Hrquestions.id == form_data.id).first()
    if form_data.question_uz is not None:
        db_question.question_uz = form_data.question_uz
    if form_data.question_ru is not None:
        db_question.question_ru = form_data.question_ru
    if form_data.answer_uz is not None:
        db_question.answer_uz = form_data.answer_uz
    if form_data.answer_ru is not None:
        db_question.answer_ru = form_data.answer_ru
    if form_data.status is not None:
        db_question.status = form_data.status
    db.commit()
    db.refresh(db_question)
    return db_question


def get_questions(db: Session, id: Optional[int] = None,sphere_id: Optional[int] = None):
    query = db.query(hr_model.Hrquestions)
    if id is not None:
        query = query.filter(hr_model.Hrquestions.id == id)
    if sphere_id is not None:
        query = query.filter(hr_model.Hrquestions.sphere_id == sphere_id)
    return query.order_by(hr_model.Hrquestions.created_at.desc()).all()


def update_complaint(db: Session, form_data: hr_schema.UpdateComplaint):
    db_complaint = db.query(hr_model.Hrcomplaints).filter(hr_model.Hrcomplaints.id == form_data.id).first()
    if form_data.tel_id is not None:
        db_complaint.hrclient_id = form_data.tel_id
    if form_data.complaint is not None:
        db_complaint.complaint = form_data.complaint
    if form_data.status is not None:
        db_complaint.status = form_data.status
    if form_data.deny_reason is not None:
        db_complaint.deny_reason = form_data.deny_reason
    if form_data.category_id is not None:
        db_complaint.category_id = form_data.category_id
    db.commit()
    db.refresh(db_complaint)
    return db_complaint



def create_communication(db:Session,url,text,hrcomplaint_id,user_id):
    db_communication = hr_model.Hrcommunications(
        url=url,
        text=text,
        hrcomplaint_id=hrcomplaint_id,
        user_id=user_id
    )
    db.add(db_communication)
    db.commit()
    db.refresh(db_communication)
    return db_communication


def get_communication(db:Session,hrcomplaint_id: Optional[int] = None,hrclient_id: Optional[int] = None,status: Optional[int] = None):
    query = db.query(hr_model.Hrcommunications).join(hr_model.Hrcomplaints)
    if hrclient_id is not None:
        query = query.filter(hr_model.Hrcomplaints.hrclient_id == hrclient_id)
    if hrcomplaint_id is not None:
        query = query.filter(hr_model.Hrcommunications.hrcomplaint_id == hrcomplaint_id)
    return query.order_by(hr_model.Hrcommunications.created_at.desc()).all()


def create_sphere(db: Session, form_data: hr_schema.SphereCreate):
    query = hr_model.Hrspheras(
        name=form_data.name,
        name_uz=form_data.name_uz,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_sphere(db:Session,id):
    query = db.query(hr_model.Hrspheras)
    if id is not None:
        query = query.filter(hr_model.Hrspheras.id == id)
    return query.all()


def get_hrclients(db:Session,id: Optional[int] = None):
    query = db.query(hr_model.Hrclients).join(hr_model.Hrcomplaints).join(hr_model.Hrcommunications)
    if id is not None:
        query = query.filter(hr_model.Hrclients.id == id)
    return query.order_by(hr_model.Hrcommunications.created_at.desc()).all()



def get_hr_clients(db:Session, spheres: Optional[list[int]] = None):
    query = db.query(hr_model.Hrclients)
    if spheres is not None:
        query = query.filter(
            and_(
                hr_model.Hrclients.status == 1,
                hr_model.Hrclients.sphere.in_(spheres)
            )
        )

    return query.order_by(hr_model.Hrclients.sphere.asc()).all()



def get_complaints(db:Session,id: Optional[int] = None,
                   hrtype: Optional[int] = None,
                   sphere_id: Optional[int] = None,
                   category_id:Optional[int]=None,
                   status:Optional[int]=None,
                   client_name:Optional[str]=None,
                   complaint:Optional[str]=None
                   ):
    query = db.query(hr_model.Hrcomplaints).join(hr_model.Hrcomplaints.hrclient)
    if id is not None:
        query = query.filter(hr_model.Hrcomplaints.id == id)
    if hrtype is not None:
        query = query.filter(hr_model.Hrcomplaints.hrtype == hrtype)
    if sphere_id is not None:
        query = query.filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
    if status is not None:
        query  =query.filter(hr_model.Hrcomplaints.status==status)
    if category_id is not None:
        query = query.filter(hr_model.Hrcomplaints.category_id== category_id)
    if client_name is not None:
        query = query.filter(hr_model.Hrclients.name.ilike(f"%{client_name}%"))
    if complaint is not None:
        query = query.filter(hr_model.Hrcomplaints.complaint.ilike(f"%{complaint}%"))
    return query.order_by(hr_model.Hrcomplaints.created_at.desc()).all()

def create_hrcategory(db: Session, form_data: hr_schema.HrCategoryCreate):
    query = hr_model.HrCategories(
        name=form_data.name,
        name_uz=form_data.name_uz,
        status=form_data.status,
        hrsphere_id=form_data.hrsphere_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_hrcategory(db: Session,id: Optional[int] = None, hrsphere_id: Optional[int] = None):
    query = db.query(hr_model.HrCategories)
    if id is not None:
        query = query.filter(hr_model.HrCategories.id == id)
    if hrsphere_id is not None:
        query = query.filter(hr_model.HrCategories.hrsphere_id == hrsphere_id)
    return query.all()


def update_hrcategory(db: Session, form_data: hr_schema.HrCategoryUpdate):
    db_category = db.query(hr_model.HrCategories).filter(hr_model.HrCategories.id == form_data.id).first()
    if form_data.name is not None:
        db_category.name = form_data.name
    if form_data.name_uz is not None:
        db_category.name_uz = form_data.name_uz
    if form_data.status is not None:
        db_category.status = form_data.status
    if form_data.hrsphere_id is not None:
        db_category.hrsphere_id = form_data.hrsphere_id

    db.commit()
    db.refresh(db_category)
    return db_category
