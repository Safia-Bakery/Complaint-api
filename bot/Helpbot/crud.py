from complaints.models.helpdesk_clients import HelpDeskClients
from complaints.models.helpdesk import HelpDeskChats
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID


def get_or_create_client(telegram_id,name):
    with SessionLocal() as db:
        query = db.query(HelpDeskClients).filter(HelpDeskClients.telegram_id==telegram_id).first()
        if query:
            return query
        else:
            query = HelpDeskClients(
                telegram_id=telegram_id,
                name=name
            )
            db.add(query)
            db.commit()
            db.refresh(query)
            return query



def get_message(message_id:int):
    with SessionLocal() as db:
        return db.query(HelpDeskChats).filter(
            HelpDeskChats.message_id==message_id
    ).first()


def create_message(client_id:int,message_text:str):
    with SessionLocal() as db:

        query = HelpDeskChats(
            comment=message_text,
            help_desk_client_id=client_id
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query


def update_messsage(message_id:int,id:int):
    with SessionLocal() as db:
        query = db.query(HelpDeskChats).filter(HelpDeskChats.id==id).first()
        query.message_id=message_id
        db.commit()
        db.refresh(query)
        return query



def get_client(message_id):
    with SessionLocal() as db:
        return db.query(HelpDeskClients).join(HelpDeskChats).filter(HelpDeskChats.message_id== message_id).first()





