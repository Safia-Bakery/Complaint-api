from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from users.schemas.user_sch import NotificationUser


class CreateNotification(BaseModel):
    text: Optional[str]
    scheduled_at: Optional[datetime] = None
    receivers_sphere: Optional[List[int]] = None



class UpdateNotification(BaseModel):
    id: int
    text: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    receivers_sphere: Optional[List[int]] = None


class Notification(BaseModel):
    id: int
    text: Optional[str] = None
    user: Optional[NotificationUser] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[int] = None
    receivers_sphere: Optional[List[int]] = None
    created_at: Optional[datetime] = None


