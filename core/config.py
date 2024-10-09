import logging
from dotenv import load_dotenv
import os

load_dotenv()


BASE_URL = os.environ.get("BASE_URL_SERVICE")
USERNAME = os.environ.get("LOGIN_SERVICE")
PASSWORD = os.environ.get("PASSWORD_SERVICE")
# ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
