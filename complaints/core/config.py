from dotenv import load_dotenv
import os

load_dotenv()


BASE_URL = os.environ.get("BASE_URL_SERVICE")
USERNAME = os.environ.get("LOGIN_SERVICE")
PASSWORD = os.environ.get("PASSWORD_SERVICE")
BOT_TOKEN_COMPLAINT= os.environ.get("BOT_TOKEN_COMPLAINT")
DOCS_USERNAME=os.environ.get('DOCS_USERNAME')
DOCS_PASSWORD=os.environ.get('DOCS_PASSWORD')
