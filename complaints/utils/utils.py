import random
import string
import requests
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from complaints.core.config import DOCS_PASSWORD,DOCS_USERNAME

security = HTTPBasic()


def file_name_generator(length=20):
    current_date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    return current_date


def sendtotelegram_inline_buttons(bot_token,chat_id,message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Yes', 'callback_data': '1'}],
            [{'text': 'No', 'callback_data': '2'}],
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False



def get_current_user_for_docs(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = DOCS_USERNAME
    correct_password = DOCS_PASSWORD
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username