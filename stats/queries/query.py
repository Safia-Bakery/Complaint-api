from complaints.models import request_model
from hrcomplaint.models import hr_model
from users.models import user_model
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
from calendar import month_name

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
import pytz
timezone_tash = pytz.timezone("Asia/Tashkent")




def get_workers_comparison_stats(db:Session):
    last_30_days = db.query(hr_model.Hrcomplaints).filter(
        hr_model.Hrcomplaints.hrtype==2,
        hr_model.Hrcomplaints.sphere_id==1,
        ).filter(hr_model.Hrcomplaints.created_at >=
        datetime.now(tz=timezone_tash) - timedelta(days=30)).count()


    last_60_and_30_days = db.query(hr_model.Hrcomplaints).filter(
        hr_model.Hrcomplaints.hrtype==2,
        hr_model.Hrcomplaints.sphere_id==1,
        ).filter(and_(
        hr_model.Hrcomplaints.created_at >=
        datetime.now(tz=timezone_tash) - timedelta(days=60),hr_model.Hrcomplaints.created_at <
        datetime.now(tz=timezone_tash) - timedelta(days=30))).count()
    change= last_30_days - last_60_and_30_days
    if last_60_and_30_days == 0:
        percentage_change = float('inf') if last_30_days > 0 else 0

    else:
        percentage_change = (change/last_60_and_30_days)*100

    return {
        "last_30_days": last_30_days,
        "last_60_and_30_days": last_60_and_30_days,
        "change": change,
        "percentage_change": percentage_change
    }


def get_complaint_service_stats(db:Session):

    last_30_days =(db.query(request_model.Complaints).
                    join(request_model.Subcategories).
                    filter(request_model.Subcategories.category_id==3).
                    filter(request_model.Complaints.created_at >=
                           datetime.now(tz=timezone_tash) - timedelta(days=30))
                   ).count()

    last_60_and_30_days = (db.query(request_model.Complaints).
                    join(request_model.Subcategories).
                    filter(request_model.Subcategories.category_id==3).
                    filter(and_(
        request_model.Complaints.created_at >= datetime.now(tz=timezone_tash) - timedelta(days=60),
        request_model.Complaints.created_at < datetime.now(tz=timezone_tash) - timedelta(days=30)
    ))
    ).count()
    change= last_30_days - last_60_and_30_days
    if last_60_and_30_days == 0:
        percentage_change = 0

    else:
        percentage_change = (change/last_60_and_30_days)*100

    return {
        "last_30_days": last_30_days,
        "last_60_and_30_days": last_60_and_30_days,
        "change": change,
        "percentage_change": percentage_change
    }


def get_complaint_quality_stats(db:Session):

    last_30_days =(db.query(request_model.Complaints).
                   join(request_model.Subcategories).
                   filter(request_model.Subcategories.category_id==1).
                    filter(request_model.Complaints.created_at >=
                           datetime.now(tz=timezone_tash) - timedelta(days=30)).count()
                   )

    last_60_and_30_days = (db.query(request_model.Complaints).
                    join(request_model.Subcategories).
                    filter(request_model.Subcategories.category_id==1).
                    filter(and_(
        request_model.Complaints.created_at >= datetime.now(tz=timezone_tash) - timedelta(days=60),
        request_model.Complaints.created_at < datetime.now(tz=timezone_tash) - timedelta(days=30)
    )).count()
                           )
    change= last_30_days - last_60_and_30_days
    if last_60_and_30_days == 0:
        percentage_change = 0

    else:
        percentage_change = (change/last_60_and_30_days)*100

    return {
        "last_30_days": last_30_days,
        "last_60_and_30_days": last_60_and_30_days,
        "change": change,
        "percentage_change": percentage_change
    }


def get_qr_client_stats(db:Session):
    last_30_days = (db.query(request_model.Complaints).
                    join(request_model.Subcategories).
                    filter(request_model.Complaints.is_client==True).
                    filter(request_model.Complaints.created_at >=
                           datetime.now(tz=timezone_tash) - timedelta(days=30)).count()
                    )

    last_60_and_30_days = (db.query(request_model.Complaints).
                           join(request_model.Subcategories).
                           filter(request_model.Complaints.is_client==True).
                           filter(and_(
        request_model.Complaints.created_at >= datetime.now(tz=timezone_tash) - timedelta(days=60),
        request_model.Complaints.created_at < datetime.now(tz=timezone_tash) - timedelta(days=30)
    )).count()
                           )
    change = last_30_days - last_60_and_30_days
    if last_60_and_30_days == 0:
        percentage_change = 0

    else:
        percentage_change = (change / last_60_and_30_days) * 100

    return {
        "last_30_days": last_30_days,
        "last_60_and_30_days": last_60_and_30_days,
        "change": change,
        "percentage_change": percentage_change
    }


def get_subcategories_stats(db: Session, from_date, to_date):
    results = (db.query(request_model.Subcategories.name, func.count(request_model.Complaints.id))
                 .join(request_model.Subcategories, request_model.Complaints.subcategory_id == request_model.Subcategories.id)
                 .filter(request_model.Complaints.created_at >= from_date)
                 .filter(request_model.Complaints.created_at <= to_date)
                 .group_by(request_model.Complaints.subcategory_id, request_model.Subcategories.name)
                 .all())

    stats = {subcategory_name: count for subcategory_name, count in results}
    return stats


def get_complaint_according_country_expenditure_stats(db: Session, from_date, to_date):
    # Query for service category (category_id == 3)
    service_stats = (db.query(request_model.Countries.name, func.coalesce(func.sum(request_model.Complaints.expense), 0))
               .outerjoin(request_model.Subcategories, request_model.Complaints.subcategory_id == request_model.Subcategories.id)
               .outerjoin(request_model.Countries, request_model.Subcategories.country_id == request_model.Countries.id)
               .filter(request_model.Complaints.created_at >= from_date)
               .filter(request_model.Complaints.created_at <= to_date)
               .filter(request_model.Subcategories.category_id == 3)
               .group_by(request_model.Countries.name)
               .all())

    service_stats = {country_name: total_expense for country_name, total_expense in service_stats}

    # Query for quality category (category_id == 1)
    quality_stats = (db.query(request_model.Countries.name, func.coalesce(func.sum(request_model.Complaints.expense), 0))
                     .outerjoin(request_model.Subcategories, request_model.Complaints.subcategory_id == request_model.Subcategories.id)
                     .outerjoin(request_model.Countries, request_model.Subcategories.country_id == request_model.Countries.id)
                     .filter(request_model.Complaints.created_at >= from_date)
                     .filter(request_model.Complaints.created_at <= to_date)
                     .filter(request_model.Subcategories.category_id == 1)
                     .group_by(request_model.Countries.name)
                     .all())

    quality_stats = {country_name: total_expense for country_name, total_expense in quality_stats}

    stats = {
        "service": service_stats,
        "quality": quality_stats
    }

    return stats




def last_6_monthly_complaint_stats(db: Session):
    now = datetime.now(tz=timezone_tash)
    six_months_ago = now - timedelta(days=180)

    # Initialize a dictionary with the last 6 months' names set to 0
    stats_service = {month_name[(now.month - i - 1) % 12 + 1]: 0 for i in range(6)}
    stats_quality = {month_name[(now.month - i - 1) % 12 + 1]: 0 for i in range(6)}




    # Query the database for the last 6 months of complaints
    # Query the database for the last 6 months of complaints
    results = (db.query(func.extract('month', request_model.Complaints.created_at).label('month'),
                        func.count(request_model.Complaints.id))
               .filter(request_model.Complaints.created_at >= six_months_ago)
               .join(request_model.Subcategories)
               .filter(request_model.Subcategories.category_id == 3)
               .group_by('month')
               .all())

    # Update the dictionary with the actual counts
    for month, count in results:
        stats_service[month_name[int(month)]] = count

    results = (db.query(func.extract('month', request_model.Complaints.created_at).label('month'),
                        func.count(request_model.Complaints.id))
               .filter(request_model.Complaints.created_at >= six_months_ago)
               .join(request_model.Subcategories)
               .filter(request_model.Subcategories.category_id == 1)
               .group_by('month')
               .all())

    for month, count in results:
        stats_quality[month_name[int(month)]] = count


    stats = {
        "service": stats_service,
        "quality": stats_quality
    }
    return stats



def get_hr_complaint_categories_stats(db: Session, from_date, to_date,sphere_id):
    results = (db.query(hr_model.HrCategories.name, func.count(hr_model.Hrcomplaints.id))
               .join(hr_model.HrCategories, hr_model.Hrcomplaints.category_id == hr_model.HrCategories.id)
               .filter(hr_model.Hrcomplaints.created_at >= from_date)
               .filter(hr_model.Hrcomplaints.created_at <= to_date)
                .filter(hr_model.Hrcomplaints.hrtype==2)
                .filter(hr_model.Hrcomplaints.sphere_id==sphere_id)
               .group_by(hr_model.Hrcomplaints.category_id, hr_model.HrCategories.name)
               .all())

    stats = {category_name: count for category_name, count in results}
    return stats




def get_hr_complaint_total_number_stats(db:Session,from_date,to_date,sphere_id):
    new = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype==2)
        .filter(hr_model.Hrcomplaints.sphere_id==sphere_id)
        .filter(hr_model.Hrcomplaints.status == 0)
        .all()
    )
    finished = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 2)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 2)
        .all()
    )
    rejected = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 2)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 3)
        .all()
    )
    data = {
        "new": new[0][0],
        "finished": finished[0][0],
        "rejected": rejected[0][0]
    }
    return data


def get_hr_question_total_number_stats(db:Session,from_date,to_date,sphere_id):
    new = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 1)
        .filter(hr_model.Hrcomplaints.sphere_id==sphere_id)
        .filter(hr_model.Hrcomplaints.status == 0)
        .all()
    )
    finished = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 1)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 2)
        .all()
    )
    rejected = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 1)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 3)
        .all()
    )
    data = {
        "new": new[0][0],
        "finished": finished[0][0],
        "rejected": rejected[0][0]
    }
    return data


def get_hr_advice_total_number_stats(db:Session,from_date,to_date,sphere_id):
    new = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 3)
        .filter(hr_model.Hrcomplaints.sphere_id==sphere_id)
        .filter(hr_model.Hrcomplaints.status == 0)
        .all()
    )
    finished = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 3)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 2)
        .all()
    )
    rejected = (
        db.query(func.count(hr_model.Hrcomplaints.id))
        .filter(hr_model.Hrcomplaints.created_at >= from_date)
        .filter(hr_model.Hrcomplaints.created_at <= to_date)
        .filter(hr_model.Hrcomplaints.hrtype == 3)
        .filter(hr_model.Hrcomplaints.sphere_id == sphere_id)
        .filter(hr_model.Hrcomplaints.status == 3)
        .all()
    )
    data = {
        "new": new[0][0],
        "finished": finished[0][0],
        "rejected": rejected[0][0]
    }
    return data


