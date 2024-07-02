from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
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

def get_country(db: Session, id: Optional[int] = None,status:Optional[int]=None):
    query = db.query(request_model.Countries)
    if id is not None:
        query = query.filter(request_model.Countries.id == id)
    if status is not None:
        query = query.filter(request_model.Countries.status == status)
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

def get_category(db: Session, id: Optional[int] = None,status:Optional[int]=None):
    query = db.query(request_model.Categories)
    if id is not None:
        query = query.filter(request_model.Categories.id == id)
    if status is not None:
        query = query.filter(request_model.Categories.status == status)
    return query.all()


def create_subcategory(db: Session, form_data: schema.CreateSubCategory):
    query = request_model.Subcategories(
        name=form_data.name,
        category_id=form_data.category_id,
        country_id=form_data.country_id,
        status=form_data.status
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
    if form_data.status is not None:
        query.status = form_data.status
    db.commit()
    db.refresh(query)
    return query


def get_subcategory(db: Session, id: Optional[int] = None,country_id: Optional[int] = None,category_id: Optional[int] = None,status:Optional[int]=None):
    query = db.query(request_model.Subcategories)
    if id is not None:
        query = query.filter(request_model.Subcategories.id == id)
    if country_id is not None:
        query = query.filter(request_model.Subcategories.country_id == country_id)
    if category_id is not None:
        query = query.filter(request_model.Subcategories.category_id == category_id)
    if status is not None:
        query = query.filter(request_model.Subcategories.status == status)

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
                    autonumber:Optional[str]=None,
                    expense:Optional[float]=None,
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
                                        expense=expense,
                                        is_client=False,
                                        status=0,
                                        is_internal=1
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


def update_complaints(db:Session,form_data:schema.UpdateComplaint,updated_by):
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
    if form_data.expense is not None:
        query.expense = form_data.expense
    if form_data.deny_reason is not None:
        query.deny_reason = form_data.deny_reason
    query.updated_by = updated_by   
    
        
    db.commit()
    db.refresh(query)
    return query


def update_statuses(db:Session,status,id,okk_status):
    query = db.query(request_model.Complaints).filter(request_model.Complaints.id==id).first()
    if status is not None:

        query.status = status
    if okk_status is not None:
        query.otk_status = okk_status
    db.commit()
    db.refresh(query)
    return query

def get_complaints(db:Session,
                   id,
                   branch_id,
                   subcategory_id,
                   status,
                   otk_status,
                   updated_by,
                   expense,
                   date_return,
                    phone_number,
                    client_name,
                    category_id,
                    country_id,
                    is_client,
                    otk,
                    is_internal
                   ):
    query = db.query(request_model.Complaints).join(request_model.Subcategories)

    if is_client is not None:
        query = query.filter(request_model.Complaints.is_client == is_client)
    if country_id is not None:
        query = query.filter(request_model.Subcategories.country_id == country_id)
    if category_id is not None:
        query = query.filter(request_model.Subcategories.category_id == category_id)
    if client_name is not None:
        query = query.filter(request_model.Complaints.client_name.ilike(f"%{client_name}%"))
    if date_return is not None:
        query = query.filter(cast(request_model.Complaints.date_return,Date) == date_return)
    if phone_number is not None:
        query = query.filter(request_model.Complaints.client_number.ilike(f"%{phone_number}%"))
    if expense is not None:
        query = query.filter(request_model.Complaints.expense == expense)
    if updated_by is not None:
        query = query.filter(request_model.Complaints.updated_by == updated_by)
    
    if id is not None:
        query = query.filter(request_model.Complaints.id == id)
    if branch_id is not None:
        query = query.filter(request_model.Complaints.branch_id == branch_id)
    if subcategory_id is not None:
        query = query.filter(request_model.Complaints.subcategory_id == subcategory_id)

    if status is not None:
        query = query.filter(request_model.Complaints.status == status)
    if is_internal is not None:
        query = query.filter(request_model.Complaints.is_internal == is_internal)
    
    if otk:
        query = query.filter(request_model.Complaints.otk_status != 0)
    elif otk_status is not None:
        query =  query.filter(request_model.Complaints.otk_status==otk_status)

   
    return query.order_by(request_model.Complaints.id.desc()).all()



def create_communication(db:Session,complaint_id:int,text:str,url:str):
    query = request_model.Communications(complaint_id=complaint_id,text=text,url=url)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_communications(db:Session,client_id,complaint_id):
    query = db.query(request_model.Communications).join(request_model.Complaints)
    if client_id is not None:
        query = query.filter(request_model.Complaints.client_id == client_id)

    if complaint_id is not None:    
        query = query.filter(request_model.Communications.complaint_id == complaint_id)

    return query.order_by(request_model.Communications.created_at.desc()).all()



