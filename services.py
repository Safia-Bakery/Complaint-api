from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import random
import string
import pandas as pd

from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    HTTPException,
    status,
)
import smtplib
from database import SessionLocal, Base,engine
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
from users.schemas import user_sch
#from schemas import user_schema
#from queries import user_query as crud
from dotenv import load_dotenv
import requests
from users.queries import query

load_dotenv()




ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY") # should be kept secret
ALGORITHM = os.environ.get("ALGORITHM")


ESKIZ_BASE_URL = os.getenv("ESKIZ_BASE_URL")
ESKIZ_LOGIN = os.getenv("ESKIZ_LOGIN")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD")


SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_USERNAME=os.getenv('SMTP_USERNAME')
FROM_EMAIL = os.getenv('FROM_EMAIL')

smtp_port = 587


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt



async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> user_sch.User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = query.get_user(db, sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    permission_list = {}
    if user.role is not None:
        for i in user.role.permission:
            permission_list[i.action_id] = True
    user.permissions = permission_list
    return user

def verify_refresh_token(refresh_token: str) -> Union[str, None]:
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            return None
    except (jwt.JWTError, ValidationError):
        return None
    return sub



def generate_random_filename(length=20):
    # Define the characters you want to use in the random filename
    characters = string.ascii_letters + string.digits

    # Generate a random filename of the specified length
    random_filename = "".join(random.choice(characters) for _ in range(length))

    return random_filename



def send_textmessage_telegram(bot_token, chat_id, message_text):
    # Create the request payload
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"}

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:

        return response
    else:
        return False



def send_file_telegram(bot_token, chat_id, file_path, caption=None, reply_to_message_id=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # 'files' for sending documents is a dictionary with a tuple (optional filename, file data)
    if file_path is None:
        return requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text": caption}).json()
    else:

        with open(file_path, 'rb') as file:
            files = {'document': (file_path, file)}
            data = {'chat_id': chat_id,'reply_to_message_id':reply_to_message_id}

            # Make a POST request to the Telegram API
            response = requests.post(url, data=data, files=files)
        return response.json()



def generate_excell( data ):
    ready_data = {
        'от гостя': {
            '№ заявки':[ ],
            "Дата поступления":   [],
            'Название магазина':   [],
             'от кого жалоба: гость или магазин':   [ ],
             'дата покупки':   [ ],
            'имя гостя, номер телефона':   [],
            'Наименование изделия/ СиМ':   [],
            'Причина жалобы':   [],
            'дата поступления в магазин':   [ ],
            'Описание жалобы':  [],
            'фото/видео?':  [],
            'дата принятия заявки':  [ ],
             'ответ магазину':  [ ],
            'номер машины/ Ф.И. водителя':  [],
            'дата поступления на фабрику':  [],
            'категория жалобы':  [],
            'Есть ли вина цеха/магазина (да/нет)':  [],
             'Номер и название виновного цеха/магазина':  [],
            'бригадир/ управляющий':  [],
             'причины':  [],
            'Корректирующие действия':  [],
            'заключение лаборатории':  [ ],
        },
        'от магазина': {
                '№ заявки': [ ],
                'Дата поступления': [],
                'Название магазина': [],
                'от кого жалоба: гость или магазин': [],
                "Причина жалобы": [],
                'Наименование изделия/ СиМ': [],
                'дата поступления в магазин': [ ],
                'Описание жалобы': [],
                 'фото/видео?': [ ],
                'дата принятия заявки': [],
                'ответ магазину': [],
                'номер машины/ Ф.И. водителя': [ ],
                 'дата поступления на фабрику': [],
                'категория жалобы': [  ],
                'Есть ли вина цеха/магазина (да/нет)': [],
                'Номер и название виновного цеха/магазина': [ ],
                 'бригадир/ управляющий': [],
                'причины': [],
                'Корректирующие действия': [ ],
            },
    }
    for i in data:
        if i.subcategory.category_id==1:
            ready_data['от гостя']['№ заявки'].append(str(i.id))
            if i.created_at is not None:
                ready_data['от гостя']['Дата поступления'].append( i.created_at.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от гостя']['Дата поступления'].append('  ')
            if i.branch_id is not None:
                ready_data['от гостя']['Название магазина'].append(i.branch.name)
            else:
                ready_data['от гостя']['Название магазина'].append('  ')

            ready_data['от гостя']['от кого жалоба: гость или магазин'].append( 'от гостя')

            if i.date_purchase is not None:
                ready_data['от гостя']['дата покупки'].append( i.date_purchase.strftime("%d.%m.%Y"))
            else:
                ready_data['от гостя']['дата покупки'].append('  ')

            if i.client_name is not None and i.client_number is not None:
                ready_data['от гостя']['имя гостя, номер телефона'].append( i.client_name + ' \n' + i.client_number)
            elif i.client_name is not None:
                ready_data['от гостя']['имя гостя, номер телефона'].append(i.client_name)

            elif i.client_number is not None:
                ready_data['от гостя']['имя гостя, номер телефона'].append(i.client_number)
            else:
                ready_data['от гостя']['имя гостя, номер телефона'].append('  ')

            if i.product_name is not None:
                ready_data['от гостя']['Наименование изделия/ СиМ'].append(i.product_name)
            else:
                ready_data['от гостя']['Наименование изделия/ СиМ'].append('  ')

            if i.comment is not None:
                ready_data['от гостя']['Причина жалобы'].append(i.subcategory.name)
            else:
                ready_data['от гостя']['Причина жалобы'].append('  ')

            if i.date_return is not None:
                 ready_data['от гостя']['дата поступления в магазин'].append( i.date_return.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от гостя']['дата поступления в магазин'].append('  ')

            if i.product_name is not None:
                ready_data['от гостя']['Описание жалобы'].append(i.comment)
            else:
                ready_data['от гостя']['Описание жалобы'].append( '  ')

            ready_data['от гостя']['фото/видео?'].append( 'не экспортировать в таблицу')

            if i.updated_at is not None:
                ready_data['от гостя']['дата принятия заявки'].append( i.updated_at.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от гостя']['дата принятия заявки'].append('  ')

            ready_data['от гостя']['ответ магазину'].append( '  ')

            if i.autonumber is not None:
                ready_data['от гостя']['номер машины/ Ф.И. водителя'].append(i.autonumber)
            else:
                ready_data['от гостя']['номер машины/ Ф.И. водителя'].append('  ')

            if i.date_return is not None:
                ready_data['от гостя']['дата поступления на фабрику'].append( i.date_return.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от гостя']['дата поступления на фабрику'].append('  ')

            if i.subcategory_id is not None:
                ready_data['от гостя']['категория жалобы'].append(i.subcategory.name)
            else:
                ready_data['от гостя']['категория жалобы'].append('  ')
            if i.producer_guilty is not None:
                if i.producer_guilty:
                    ready_data['от гостя']['Есть ли вина цеха/магазина (да/нет)'].append( 'да')
                else:
                    ready_data['от гостя']['Есть ли вина цеха/магазина (да/нет)'].append('нет')
            else:
                ready_data['от гостя']['Есть ли вина цеха/магазина (да/нет)'].append('  ')

            ready_data['от гостя']['Номер и название виновного цеха/магазина'].append('  ')
            ready_data['от гостя']['бригадир/ управляющий'].append('  ')

            ready_data['от гостя']['причины'].append('  ')

            if i.corrections is not None:
                ready_data['от гостя']['Корректирующие действия'].append(i.corrections)
            else:
                ready_data['от гостя']['Корректирующие действия'].append('  ')

            ready_data['от гостя']['заключение лаборатории'].append('  ')
        elif i.subcategory.category_id==5:
            ready_data['от магазина']['№ заявки'].append(str(i.id))
            if i.created_at is not None:
                ready_data['от магазина']['Дата поступления'].append(i.created_at.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от магазина']['Дата поступления'].append('  ')
            if i.branch_id is not None:
                ready_data['от магазина']['Название магазина'].append( i.branch.name)
            else:
                ready_data['от магазина']['Название магазина'].append('  ')

            ready_data['от магазина']['от кого жалоба: гость или магазин'].append('от магазина')

            if i.product_name is not None:
                ready_data['от магазина']['Причина жалобы'].append(i.subcategory.name)
            else:
                ready_data['от магазина']['Причина жалобы'].append('  ')

            if i.product_name is not None:
                ready_data['от магазина']['Наименование изделия/ СиМ'].append(i.product_name)
            else:
                ready_data['от магазина']['Наименование изделия/ СиМ'].append('  ')

            if i.date_return is not None:
                ready_data['от магазина']['дата поступления в магазин'].append(i.date_return.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от магазина']['дата поступления в магазин'].append('  ')

            if i.comment is not None:
                ready_data['от магазина']['Описание жалобы'].append(i.comment)
            else:
                ready_data['от магазина']['Описание жалобы'].append('  ')

            ready_data['от магазина']['фото/видео?'].append( 'не экспортировать в таблицу')

            if i.updated_at is not None:
                ready_data['от магазина']['дата принятия заявки'].append( i.updated_at.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от магазина']['дата принятия заявки'].append('  ')

            ready_data['от магазина']['ответ магазину'].append('  ')

            if i.autonumber is not None:
                ready_data['от магазина']['номер машины/ Ф.И. водителя'].append( i.autonumber)
            else:
                ready_data['от магазина']['номер машины/ Ф.И. водителя'].append('  ')

            if i.date_return is not None:
                ready_data['от магазина']['дата поступления на фабрику'].append(i.date_return.strftime("%d.%m.%Y %H:%M"))
            else:
                ready_data['от магазина']['дата поступления на фабрику'].append('  ')

            if i.subcategory_id is not None:
                ready_data['от магазина']['категория жалобы'].append( ' ')
            else:
                ready_data['от магазина']['категория жалобы'].append('  ')


            if i.producer_guilty is not None:
                if i.producer_guilty:
                    ready_data['от магазина']['Есть ли вина цеха/магазина (да/нет)'].append('да')
                else:
                    ready_data['от магазина']['Есть ли вина цеха/магазина (да/нет)'].append( 'нет')
            else:
                ready_data['от магазина']['Есть ли вина цеха/магазина (да/нет)'].append('  ')

            ready_data['от магазина']['Номер и название виновного цеха/магазина'].append('  ')
            ready_data['от магазина']['бригадир/ управляющий'] .append('  ')

            ready_data['от магазина']['причины'].append('  ')

            if i.corrections is not None:
                ready_data['от магазина']['Корректирующие действия'].append(i.corrections)
            else:
                ready_data['от магазина']['Корректирующие действия'].append('  ')

    filename = 'files/дкк отчёт ' +  datetime.now().strftime("%d.%m.%Y") + '.xlsx'

    with pd.ExcelWriter(filename , engine='xlsxwriter') as writer:
        for key, value in ready_data.items():
            pd.DataFrame(value).to_excel(writer, sheet_name=str(key[:30]))
    return filename



















