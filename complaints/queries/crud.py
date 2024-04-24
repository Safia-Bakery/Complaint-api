from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from complaints.models import request_model
from complaints.schemas import schema   
from complaints.models.request_model import Branchs,Communications


def create_country(db: Session, form_data: schema.CreateCountry):
    query = request_model.Countries(
        name=form_data.name,
        code=form_data.code,
        status=form_data.status,
        service_id=form_data.service_id,
        quality_id=form_data.quality_id,
        callcenter_id=form_data.callcenter_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_country(db:Session,form_data:schema.UpdateCountry):
    query = db.query(request_model.Countries).filter(request_model.Countries.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    if form_data.code is not None:
        query.code = form_data.code
    if form_data.status is not None:
        query.status = form_data.status
    if form_data.service_id is not None:
        query.service_id = form_data.service_id
    if form_data.quality_id is not None:
        query.quality_id = form_data.quality_id
    if form_data.callcenter_id is not None:
        query.callcenter_id = form_data.callcenter_id
    db.commit()
    db.refresh(query)
    return query

def get_country(db: Session, id: Optional[int] = None):
    query = db.query(request_model.Countries)
    if id is not None:
        query = query.filter(request_model.Countries.id == id)
    return query.all()


def create_category(db: Session, form_data: schema.CreateCategory):
    query = request_model.Categories(
        name=form_data.name,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_category(db:Session,form_data:schema.UpdateCategory):
    query = db.query(request_model.Categories).filter(request_model.Categories.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    if form_data.status is not None:
        query.status = form_data.status
    db.commit()
    db.refresh(query)
    return query

def get_category(db: Session, id: Optional[int] = None):
    query = db.query(request_model.Categories)
    if id is not None:
        query = query.filter(request_model.Categories.id == id)
    return query.all()


def create_subcategory(db: Session, form_data: schema.CreateSubCategory):
    query = request_model.Subcategories(
        name=form_data.name,
        category_id=form_data.category_id,
        country_id=form_data.country_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_subcategory(db:Session,form_data:schema.UpdateSubCategory):
    query = db.query(request_model.Subcategories).filter(request_model.Subcategories.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    if form_data.category_id is not None:
        query.category_id = form_data.category_id
    if form_data.country_id is not None:
        query.country_id = form_data.country_id
    db.commit()
    db.refresh(query)
    return query


def get_subcategory(db: Session, id: Optional[int] = None):
    query = db.query(request_model.Subcategories)
    if id is not None:
        query = query.filter(request_model.Subcategories.id == id)
    return query.all()



def create_branch(db: Session, form_data: schema.CreateBranch):
    query = request_model.Branchs(
        name=form_data.name,
        status=form_data.status,
        country_id=form_data.country_id,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_branch(db:Session,form_data:schema.UpdateBranch):
    query = db.query(request_model.Branchs).filter(request_model.Branchs.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    if form_data.status is not None:
        query.status = form_data.status
    if form_data.country_id is not None:
        query.country_id = form_data.country_id
    db.commit()
    db.refresh(query)
    return query

def get_branch(db: Session, id: Optional[int] = None,name: Optional[str] = None,status: Optional[int] = None,country_id: Optional[int] = None):
    query = db.query(request_model.Branchs)
    if id is not None:
        query = query.filter(request_model.Branchs.id == id)

    if name is not None:
        query = query.filter(request_model.Branchs.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(request_model.Branchs.status == status)
    if country_id is not None:
        query = query.filter(request_model.Branchs.country_id == country_id)
    return query.all()


def update_branch_pass(db:Session,id,password):
    query = db.query(request_model.Branchs).filter(request_model.Branchs.id==id).first()
    query.password = password
    db.commit()
    db.refresh(query)
    return query


def create_complaint(db:Session,product_name:Optional[str]=None,
                     branch_id:Optional[int]=None,
                     subcategory_id:Optional[int]=None,
                     client_name:Optional[str]=None,
                     client_number:Optional[str]=None,
                     client_gender:Optional[str]=None,
                     date_purchase:Optional[datetime]=None,
                    date_return:Optional[datetime]=None,
                    comment:Optional[str]=None,
                    autonumber:Optional[str]=None
                     ):
    query = request_model.Complaints(product_name=product_name,
                                        branch_id=branch_id,
                                        subcategory_id=subcategory_id,
                                        client_name=client_name,
                                        client_number=client_number,
                                        client_gender=client_gender,
                                        date_purchase=date_purchase,
                                        date_return=date_return,
                                        comment=comment,
                                        autonumber=autonumber,

                                     )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_file(db:Session,complaint_id:int,file_path:str):
    query = request_model.Files(complaint_id=complaint_id,url=file_path)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_complaints(db:Session,form_data:schema.UpdateComplaint):
    query = db.query(request_model.Complaints).filter(request_model.Complaints.id==form_data.id).first()
    if form_data.product_name is not None:
        query.product_name = form_data.product_name
    if form_data.client_name is not None:
        query.client_name = form_data.client_name
    if form_data.client_number is not None:
        query.client_number = form_data.client_number
    if form_data.client_gender is not None:
        query.client_gender = form_data.client_gender
    if form_data.date_purchase is not None:
        query.date_purchase = form_data.date_purchase
    if form_data.date_return is not None:

        query.date_return = form_data.date_return
    if form_data.comment is not None:
        query.comment = form_data.comment
    if form_data.otk_status is not None:
        query.otk_status = form_data.otk_status
    if form_data.status is not None:
        query.status = form_data.status
    if form_data.corrections is not None:
        query.corrections = form_data.corrections

    if form_data.autonumber is not None:
        query.autonumber = form_data.autonumber
    if form_data.subcategory_id is not None:
        query.subcategory_id = form_data.subcategory_id
    if form_data.branch_id is not None:
        query.branch_id = form_data.branch_id
    db.commit()
    db.refresh(query)
    return query

    
        