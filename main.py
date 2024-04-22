from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from typing import Optional

from fastapi_pagination import paginate,Page,add_pagination
from fastapi.staticfiles import StaticFiles
from database import Base
from database import engine
from users.routes.user_routes import user_router
from hrcomplaint.routes.hr_routes import hr_router
from complaints.routes.route import complain_router
#from routes import user_route,product_route

app = FastAPI()

app.title = "Safia FastApi App"
app.version = "0.0.1"

app.include_router(user_router, tags=["User"])
app.include_router(hr_router, tags=["HR"])
app.include_router(complain_router, tags=["Complaint"])

#app.include_router(user_router)
from users.models import user_model
from hrcomplaint.models import hr_model
from complaints.models import request_model
Base.metadata.create_all(bind=engine)
app.mount("/files", StaticFiles(directory="files"), name="files")
#app.include_router(user_route.user_router, tags=["User"])
#app.include_router(product_route.product_router, tags=["Product"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/", tags=["Home"])
def message():
    """message get method"""
    return HTMLResponse("<h1>Fuck of man!</h1>")


add_pagination(app)

