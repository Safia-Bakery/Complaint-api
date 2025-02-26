from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
load_dotenv()  # Load environment variables from .env




SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()

#
# #add comment
#
#
#
# from users.models.user_model import Pages, Actions, Roles, Permissions, Users
# from hrcomplaint.models.hr_model import (Hrspheras,
#                                          HrCategories,
#                                          Hrcomplaints,
#                                          Hrclients,
#                                          Hrcommunications,
#                                          Hrquestions,
#                                          )
# from complaints.models.request_model import (
# Countries,
# Categories,
# Subcategories,
# Branchs,
# Complaints,
# Ratings,
# Files,
# Communications,
#
# )
# from complaints.models.helpdesk_clients import HelpDeskClients
# from complaints.models.helpdesk import HelpDeskChats
# from complaints.models.iikofolders import IikoFolders
# from complaints.models.iikoproducts import IikoProducts
# from complaints.models.complaint_products import ComplaintProducts
# from complaints.models.complaint_stampers import ComplaintStampers
