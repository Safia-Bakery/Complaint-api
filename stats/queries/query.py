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




