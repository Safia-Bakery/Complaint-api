
import os
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from services import (
    get_db,
    get_current_user
)

load_dotenv()
from users.schemas import user_sch
from services import generate_excell

from complaints.queries.complaints_excell_filter import filter_complaints

BOT_TOKEN_HR = os.getenv("BOT_TOKEN_HR")
BOT_TOKEN_COMPLAINT = os.getenv("BOT_TOKEN_COMPLAINT")





excell_router = APIRouter()


@excell_router.get("/complaints/excell",)
async def read_complaints(
        otk_status : Optional[int] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,

        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = filter_complaints(db=db, otk_status=otk_status, from_date=from_date, to_date=to_date)
    if len(query) == 0:
        return {"message":"No data found"}
    filename = generate_excell(query)

    return {"filename":filename}

