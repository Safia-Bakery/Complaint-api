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
            "1":[
                'автоматически',
                '№ заявки',
            ],
            "2":   [
                'автоматически в день заполнения заявки',
                'Дата:',
            ],
            "3":   [
                'заполняет тот, кто подает заявку',
                'Название магазина'
            ],
            "4":   [
                'заполняет тот, кто подает заявку',
                'от кого жалоба: гость или магазин'
            ],
            "5":   [
                'дата покупки',
                '  '
            ],
            "6":   [
                'заполняет тот, кто подает заявку',
                'имя гостя, номер телефона',
            ],
            "7":   [
                'заполняет тот, кто подает заявку',
                'Наименование изделия/ СиМ',
            ],
            "8":   [
                'заполняет тот, кто подает заявку',
                'Причина жалобы',
            ],
            "9":   [
                'заполняет тот, кто подает заявку',
                'дата поступления в магазин',
            ],
            "10":  [
                'заполняет тот, кто подает заявку',
                'Описание жалобы',
            ],
            "11":  [
                'заполняет тот, кто подает заявку',
                'фото/видео?',
            ],
            "12":  [
                'автоматически во время нажатия в обработке',
                'дата принятия заявки',
            ],
            "13":  [
                'заполняет отдел качества',
                'ответ магазину',
            ],
            "14":  [
                'заполняет тот, кто подает заявку',
                'номер машины/ Ф.И. водителя',
            ],
            "15":  [
                'автоматически после нажатия принят товар',
                'дата поступления на фабрику',
            ],
            "16":  [
                'заполняет отдел качества',
                'категория жалобы',
            ],
            "17":  [
                'заполняет отдел качества',
                'Есть ли вина цеха/магазина (да/нет)',
            ],
            "18":  [
                'заполняет отдел качества',
                'Номер и название виновного цеха/магазина',
            ],
            "19":  [
                'заполняет отдел качества',
                'бригадир/ управляющий'
            ],
            "20":  [
                'заполняет отдел качества',
                'причины',
            ],
            "21":  [
                'заполняет отдел качества',
                'Корректирующие действия'
            ],
            "22":  [
                'текст для гостя для заключения',
                'заключение лаборатории'
            ],
        },
        'от магазина': {
                "1": [
                    'автоматически',
                    '№ заявки',
                ],
                "2": [
                    'автоматически в день заполнения заявки',
                    'Дата:',
                ],
                "3": [
                    'заполняет тот, кто подает заявку',
                    'Название магазина'
                ],
                "4": [
                    'заполняет тот, кто подает заявку',
                    'от кого жалоба: гость или магазин'
                ],

                "5": [
                    'заполняет тот, кто подает заявку',
                    'Причина жалобы',
                ],
                "6": [
                    'заполняет тот, кто подает заявку',
                    'Наименование изделия/ СиМ',
                ],
                "7": [
                    'заполняет тот, кто подает заявку',
                    'дата поступления в магазин',
                ],
                "8": [
                    'заполняет тот, кто подает заявку',
                    'Описание жалобы',
                ],
                "9": [
                    'заполняет тот, кто подает заявку',
                    'фото/видео?',
                ],
                "10": [
                    'автоматически во время нажатия в обработке',
                    'дата принятия заявки',
                ],
                "11": [
                    'заполняет отдел качества',
                    'ответ магазину',
                ],
                "12": [
                    'заполняет тот, кто подает заявку',
                    'номер машины/ Ф.И. водителя',
                ],
                "13": [
                    'автоматически после нажатия принят товар',
                    'дата поступления на фабрику',
                ],
                "14": [
                    'заполняет отдел качества',
                    'категория жалобы',
                ],
                "15": [
                    'заполняет отдел качества',
                    'Есть ли вина цеха/магазина (да/нет)',
                ],
                "16": [
                    'заполняет отдел качества',
                    'Номер и название виновного цеха/магазина',
                ],
                "17": [
                    'заполняет отдел качества',
                    'бригадир/ управляющий'
                ],
                "18": [
                    'заполняет отдел качества',
                    'причины',
                ],
                "19": [
                    'заполняет отдел качества',
                    'Корректирующие действия'
                ],
            },
    }
    for i in data:
        if i.is_client:

            ready_data['от гостя']['1'] = i.id
            if i.created_at is not None:
                ready_data['от гостя']['2'] =  i.created_at.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от гостя']['2'] = '  '
            if i.branch_id is not None:
                ready_data['от гостя']['3'] = i.branch.name
            else:
                ready_data['от гостя']['3'] = '  '

            ready_data['от гостя']['4'] = 'от гостя'

            if i.date_purchase is not None:
                ready_data['от гостя']['5'] = i.date_purchase.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от гостя']['5'] = '  '

            if i.client_name is not None:
                ready_data['от гостя']['6'] = i.client_name + ' \n' + i.client_number
            else:
                ready_data['от гостя']['6'] = '  '

            if i.product_name is not None:
                ready_data['от гостя']['7'] = i.product_name
            else:
                ready_data['от гостя']['7'] = '  '

            if i.comment is not None:
                ready_data['от гостя']['8'] = i.comment
            else:
                ready_data['от гостя']['8'] = '  '

            if i.date_return is not None:
                 ready_data['от гостя']['9'] = i.date_return.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от гостя']['9'] = '  '

            if i.product_name is not None:
                ready_data['от гостя']['10'] = i.product_name
            else:
                ready_data['от гостя']['10'] = '  '

            ready_data['от гостя']['11'] = 'не экспортировать в таблицу'

            if i.updated_at is not None:
                ready_data['от гостя']['12'] = i.updated_at.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от гостя']['12'] = ' '

            ready_data['от гостя']['13'] = ' '

            if i.autonumber is not None:
                ready_data['от гостя']['14'] = i.autonumber
            else:
                ready_data['от гостя']['14'] = '  '

            if i.date_return is not None:
                ready_data['от гостя']['15'] = i.date_return.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от гостя']['15'] = '  '

            if i.subcategory_id is not None:
                ready_data['от гостя']['16'] = i.subcategory.name
            else:
                ready_data['от гостя']['16'] = '  '
            if i.producer_guilty is not None:
                if i.producer_guilty:
                    ready_data['от гостя']['17'] = 'да'
                else:
                    ready_data['от гостя']['17'] = 'нет'
            else:
                ready_data['от гостя']['17'] = '  '

            ready_data['от гостя']['18'] = '  '
            ready_data['от гостя']['19'] = '  '

            ready_data['от гостя']['20'] = '  '

            if i.corrections is not None:
                ready_data['от гостя']['21'] = i.corrections
            else:
                ready_data['от гостя']['21'] = '  '

            ready_data['от гостя']['22'] = '  '
        else:
            ready_data['от магазина']['1'] = i.id
            if i.created_at is not None:
                ready_data['от магазина']['2'] = i.created_at.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от магазина']['2'] = '  '
            if i.branch_id is not None:
                ready_data['от магазина']['3'] = i.branch.name
            else:
                ready_data['от магазина']['3'] = '  '

            ready_data['от магазина']['4'] = 'от магазина'

            if i.product_name is not None:
                ready_data['от магазина']['5'] = i.product_name
            else:
                ready_data['от магазина']['5'] = '  '

            if i.product_name is not None:
                ready_data['от магазина']['6'] = i.product_name
            else:
                ready_data['от магазина']['6'] = '  '

            if i.date_return is not None:
                ready_data['от магазина']['7'] = i.date_return.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от магазина']['7'] = '  '

            if i.comment is not None:
                ready_data['от магазина']['8'] = i.comment
            else:
                ready_data['от магазина']['8'] = '  '

            ready_data['от магазина']['9'] = 'не экспортировать в таблицу'

            if i.updated_at is not None:
                ready_data['от магазина']['10'] = i.updated_at.strftime("%Y-%m-%d %H:%M")
            else:
                ready_data['от магазина']['10'] = ' '

            ready_data['от магазина']['11'] = ' '

            if i.autonumber is not None:
                ready_data['от магазина']['12'] = i.autonumber
            else:
                ready_data['от магазина']['12'] = '  '

            if i.date_return is not None:
                ready_data['от магазина']['13'] = i.date_return.strftime("%Y-%m-%d %H:%M")

            if i.subcategory_id is not None:
                ready_data['от магазина']['14'] = i.subcategory.name

            if i.producer_guilty is not None:
                if i.producer_guilty:
                    ready_data['от магазина']['15'] = 'да'
                else:
                    ready_data['от магазина']['15'] = 'нет'
            else:
                ready_data['от магазина']['15'] = '  '

            ready_data['от магазина']['16'] = '  '
            ready_data['от магазина']['17'] = '  '

            ready_data['от магазина']['18'] = '  '

            if i.corrections is not None:
                ready_data['от магазина']['19'] = i.corrections
            else:
                ready_data['от магазина']['19'] = '  '

    filename = 'files/ТЗ для бота Жалобы ' +  datetime.now().strftime("%Y-%m-%d") + '.xlsx'

    with pd.ExcelWriter(filename , engine='xlsxwriter') as writer:
        for key,value in ready_data.items():
            pd.DataFrame(value).to_excel(writer,sheet_name=str(key[:30]))
    return filename



















