from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from users.models.user_model import Users,Roles
from users.models import user_model
from users.schemas import user_sch


def get_has_stamp(db: Session):
    return db.query(Roles).filter(Roles.has_stamp == 1).all()


