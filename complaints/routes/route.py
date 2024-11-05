from fastapi import APIRouter
from typing import TypeVar
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Form, UploadFile
from fastapi_pagination import paginate, Page
from typing import Annotated
from datetime import datetime
from services import (
    get_db,
    get_current_user,
    generate_random_filename,
    send_file_telegram,
    send_textmessage_telegram

)
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from typing import Optional

from dotenv import load_dotenv
import os

load_dotenv()
from complaints.queries import crud
from users.schemas import user_sch
from complaints.schemas import schema

T = TypeVar("T")

BOT_TOKEN_HR = os.getenv("BOT_TOKEN_HR")
BOT_TOKEN_COMPLAINT = os.getenv("BOT_TOKEN_COMPLAINT")

custompage = CustomizedPage[
    Page[T],
    UseParamsFields(size=1000)
]

complain_router = APIRouter()


@complain_router.post("/country", summary="Create country", tags=["Complaint"], response_model=schema.Country)
async def create_country(
        form_data: schema.CreateCountry,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_country(db, form_data)


@complain_router.put("/country", summary="Update country", tags=["Complaint"], response_model=schema.Country)
async def update_country(
        form_data: schema.UpdateCountry,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_country(db, form_data)


@complain_router.get("/country", summary="Get country", tags=["Complaint"], response_model=Page[schema.Country])
async def get_country(
        id: Optional[int] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_country(db, id=id, status=status))


@complain_router.post("/category", summary="Create category", tags=["Complaint"], response_model=schema.Category)
async def create_category(
        form_data: schema.CreateCategory,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_category(db, form_data)


@complain_router.put("/category", summary="Update category", tags=["Complaint"], response_model=schema.Category)
async def update_category(
        form_data: schema.UpdateCategory,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_category(db, form_data)


@complain_router.get("/category", summary="Get category", tags=["Complaint"], response_model=list[schema.Category])
async def get_category(
        id: Optional[int] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.get_category(db, id, status)


@complain_router.post("/sub-category", summary="Create sub-category", tags=["Complaint"],
                      response_model=schema.SubCategory)
async def create_sub_category(
        form_data: schema.CreateSubCategory,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_subcategory(db, form_data)


@complain_router.put("/sub-category", summary="Update sub-category", tags=["Complaint"],
                     response_model=schema.SubCategory)
async def update_sub_category(
        form_data: schema.UpdateSubCategory,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.update_subcategory(db, form_data)


@complain_router.get("/sub-category", summary="Get sub-category", tags=["Complaint"],
                     response_model=Page[schema.SubCategory])
async def get_sub_category(
        category_id: Optional[int] = None,
        id: Optional[int] = None,
        country_id: Optional[int] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return paginate(
        crud.get_subcategory(db=db, id=id, category_id=category_id, country_id=country_id, status=status))


@complain_router.post("/branches", summary="Create branches", tags=["Complaint"], response_model=schema.Branchs)
async def create_branch(
        form_data: schema.CreateBranch,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.create_branch(db, form_data)
    password = generate_random_filename(length=20) + str(query.id)
    updated_password = crud.update_branch_pass(db, query.id, password=password)
    return updated_password


@complain_router.put("/branches", summary="Update branches", tags=["Complaint"], response_model=schema.Branchs)
async def update_branch(
        form_data: schema.UpdateBranch,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_branch(db, form_data)
    return query


@complain_router.get("/branches", summary="Get branches", tags=["Complaint"], response_model=custompage[schema.Branchs])
async def get_branch(
        id: Optional[int] = None,
        name: Optional[str] = None,
        status: Optional[int] = None,
        country_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_branch(db, id=id, name=name, status=status, country_id=country_id))


@complain_router.post("/complaints", summary="Create complaint", tags=["Complaint"], response_model=schema.Complaints)
async def create_complaint(
        files: list[UploadFile] = None,
        product_name: Annotated[str, Form(...)] = None,
        client_name: Annotated[str, Form(...)] = None,
        client_number: Annotated[str, Form(...)] = None,
        client_gender: Annotated[str, Form(...)] = None,
        date_purchase: Annotated[datetime, Form(...)] = None,
        date_return: Annotated[datetime, Form(...)] = None,
        comment: Annotated[str, Form(...)] = None,
        autonumber: Annotated[str, Form(...)] = None,
        subcategory_id: Annotated[int, Form(...)] = None,
        branch_id: Annotated[int, Form(...)] = None,
        expense: Annotated[float, Form(...)] = None,
        db: Session = Depends(get_db)):
    create_complaint = crud.create_complaint(db, product_name=product_name,
                                             branch_id=branch_id,
                                             subcategory_id=subcategory_id,
                                             client_name=client_name,
                                             client_number=client_number,
                                             client_gender=client_gender,
                                             date_purchase=date_purchase,
                                             date_return=date_return,
                                             comment=comment,
                                             autonumber=autonumber,
                                             expense=expense)
    if files:
        for file in files:
            file_path = f"files/{generate_random_filename()}{file.filename}"

            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)

            crud.create_file(db=db, complaint_id=create_complaint.id, file_path=file_path)

    text_to_send = f"""
📁{create_complaint.subcategory.category.name}
🔘Категория: {create_complaint.subcategory.name}
🧑‍💼Имя: {create_complaint.client_name}
📞Номер: +{create_complaint.client_number}
📍Филиал: {create_complaint.branch.name}
🍰Блюдо: {create_complaint.product_name}
🕘Дата покупки: {create_complaint.date_purchase}
🚛Дата отправки: {create_complaint.date_return}\n
💬Комментарии: {create_complaint.comment}
            """
    call_center_id = create_complaint.subcategory.country.callcenter_id
    if create_complaint.subcategory.category_id == 5:
        chat_id = '-1001375080908'
    else:
        chat_id = call_center_id

    if not create_complaint.file:
        send_textmessage_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=chat_id, message_text=text_to_send)

    else:
        # send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=call_center_id, file_path=create_complaint.file[0].url,
        #                        caption=text_to_send)

        message_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=chat_id,
                                            file_path=None, caption=text_to_send)


        for i in create_complaint.file:
            file_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=chat_id, file_path=i.url,
                                             caption=None, reply_to_message_id=message_sended['result']['message_id'])

    return create_complaint


@complain_router.put("/complaints", summary="Update complaint", tags=["Complaint"], response_model=schema.Complaints)
async def update_complaint(
        form_data: schema.UpdateComplaint,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    # if form_data.status ==1:
    #    complaint = complaints.get_complaints(db=db,id=form_data.id)
    #    if complaint.status == 0:
    #        send_textmessage_telegram()
    query = crud.update_complaints(db, form_data, updated_by=current_user.name)

    service_id = query.subcategory.country.service_id
    quality_id = query.subcategory.country.quality_id
    if form_data.status == 1:
        text_to_send = f"""
📁{query.subcategory.category.name}
🔘Категория: {query.subcategory.name}
🧑‍💼Имя: {query.client_name}
📍Филиал: {query.branch.name}
🍰Блюдо: {query.product_name}
🕘Дата покупки: {query.date_purchase}
🚛Дата отправки: {query.date_return}\n
💬Комментарии: {query.comment}
            """
        if not query.file:
            if query.subcategory.category_id in [1, 5]:
                send_textmessage_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id, message_text=text_to_send)
            else:
                send_textmessage_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id, message_text=text_to_send)
        else:
            if query.subcategory.category_id in [1, 5]:
                message_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id,
                                                    file_path=None, caption=text_to_send)

                for i in query.file:
                    file_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=quality_id, file_path=i.url,
                                                     caption=None,
                                                     reply_to_message_id=message_sended['result']['message_id'])
            else:
                message_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id,
                                                    file_path=None, caption=text_to_send)
                for i in query.file:
                    file_sended = send_file_telegram(bot_token=BOT_TOKEN_COMPLAINT, chat_id=service_id, file_path=i.url,
                                                     caption=None,
                                                     reply_to_message_id=message_sended['result']['message_id'])

    if form_data.status == 1 and query.subcategory.category_id in [1, 5]:
        crud.update_statuses(db=db, id=query.id, otk_status=1)

    # if status is one send message to channel
    # if complaint category_id is equal to one thend send message to quality group
    # if complaint category_id is equal to 2 then send message to service group

    return query


@complain_router.get("/complaints", summary="Get complaint", tags=["Complaint"], response_model=Page[schema.Complaints])
async def get_complaints(
        id: Optional[int] = None,
        country_id: Optional[int] = None,
        category_id: Optional[int] = None,
        client_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        date_return: Optional[datetime] = None,
        expense: Optional[float] = None,
        updated_by: Optional[str] = None,
        subcategory_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        status: Optional[int] = None,
        otk_status: Optional[int] = None,
        otk: Optional[bool] = False,
        is_client: Optional[bool] = False,
        is_internal: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_complaints(db=db,
                                              id=id,
                                              subcategory_id=subcategory_id,
                                              branch_id=branch_id,
                                              otk_status=otk_status,
                                              status=status,
                                              category_id=category_id,
                                              country_id=country_id,
                                              client_name=client_name,
                                              phone_number=phone_number,
                                              date_return=date_return,
                                              expense=expense,
                                              updated_by=updated_by,
                                              is_client=is_client,
                                              otk=otk,
                                              is_internal=is_internal
                                              ))


@complain_router.post("/communications", summary="Create communication", tags=["Complaint"],
                      response_model=schema.Communications)
async def create_communication(
        file: UploadFile = None,
        complaint_id: Annotated[int, Form()] = None,
        text: Annotated[str, Form()] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    complaint_data = crud.get_complaints(db=db, id=complaint_id)
    if not complaint_data[0].client_id:
        raise HTTPException(status_code=400, detail="Client not found. You cannot send message to this complaint")

    if file is not None:
        file_path = f"files/{generate_random_filename()}{file.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None

    return crud.create_communication(db=db, complaint_id=complaint_id, text=text, url=file_path)


@complain_router.get("/communications", summary="Get communication", tags=["Complaint"],
                     response_model=Page[schema.Communications])
async def get_communication(
        complaint_id: Optional[int] = None,
        client_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return paginate(crud.get_communications(db=db, complaint_id=complaint_id, client_id=client_id))
