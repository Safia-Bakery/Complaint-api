
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
from complaints.models.request_model import Complaints


def filter_complaints(db:Session,otk_status,from_date,to_date):
    query = db.query(Complaints).filter(Complaints.status==1)
    if otk_status is not None:
        query = query.filter(Complaints.otk_status == otk_status)
    else:
        query = query.filter(Complaints.otk_status != 0)
    if from_date is not None:
        query = query.filter(Complaints.created_at >= from_date)
    if to_date is not None:
        query = query.filter(Complaints.created_at <= to_date)
    return query.all()



