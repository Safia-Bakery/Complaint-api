import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')
from bot.Complaintbot.service import transform_list

from telegram.constants import ParseMode
import os
from telegram import ReplyKeyboardMarkup,Update,WebAppInfo,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,PicklePersistence

)

from database import SessionLocal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
import database
from fastapi import Depends
from bot.Complaintbot.queries import crud
load_dotenv()

db = SessionLocal()
backend_location = 'app/'

BOTTOKEN = os.environ.get('BOT_TOKEN_COMPLAINT')
persistence = PicklePersistence(filepath='complaint.pickle')
MANU, BRANCH,SETTINGS,CATEGORY,SUBCATEGORY,NAME,PHONENUMBER,COMMENT,PHOTO,DATEPURCHASE,DATERETURN= range(1)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    user = update.message.from_user
    client = crud.get_client(db=db,id=user.id)
    if client:
        update.message.reply_text(
            f"Привет. Это корпоративный телеграм бот для оформления жалоб. 
Пожалуйста введите пароль который вы получили от системного администратора",
        )
        return BRANCH
    else:
        crud.create_client(db=db,name=user.first_name,id=user.id)
        update.message.reply_text(
            f"Привет. Это корпоративный телеграм бот для оформления жалоб. 
Пожалуйста введите пароль который вы получили от системного администратора",

        )
        return BRANCH
    

async def branch(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    input_data = update.message.text    
    branch_name = crud.get_branchs(db=db,password=input_data)
    if branch_name:
        update.message.reply_text(
            f"Ваш филиал - {branch_name.name}",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        context.user_data['branch_name'] = branch_name.name
        context.user_data['branch_id'] = branch_name.id
        return MANU
    else:
        update.message.reply_text(
            f"Пароль не верный. Попробуйте еще раз",
        )
        return BRANCH
    






async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    input_data = update.message.text
    if input_data == "Оформить жалобу":
        categories = crud.get_category(db=db)
        buttons = transform_list(categories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        update.message.reply_text(
        'Выберите категорию жалобы',
        reply_markup=reply_markup
    )
        return CATEGORY
    elif input_data == "Настройки":
        update.message.reply_text(
            f"Пожалуйста введите пароль который вы получили от системного администратора",
            reply_markup=ReplyKeyboardMarkup([['Branch','⬅️Назад']],resize_keyboard=True)
        )
        return  SETTINGS
    else:
        update.message.reply_text(
            f"Выберите категорию жалобы",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU





async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db):
    text = update.message.text
    if text == '⬅️Назад':
        update.message.reply_text(
            'Manu',
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU

    elif text == 'Branch':
        update.message.reply_text(
            'Введите пароль',
            reply_markup=ReplyKeyboardRemove()
        )
        return BRANCH
    else:
        update.message.reply_text(
            'Manu',
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    


def category(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db):
    input_text = update.message.text
    category = crud.get_category(db=db,name=input_text)
    if category:
        context.user_data['category_id'] = category.id
        subcategories = category.subcategory
        buttons = transform_list(subcategories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        update.message.reply_text(
            'Выберите подкатегорию жалобы',
            reply_markup=reply_markup
        )
        return SUBCATEGORY
    else:

        categories = crud.get_category(db=db)
        buttons = transform_list(categories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        update.message.reply_text(
        'Выберите категорию жалобы',
        reply_markup=reply_markup)
        return CATEGORY
    

def subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db):
    data = update.message.text
    subcategory = crud.get_subcategory(db=db,name=data,category_id=context.user_data['category_id'])
    if subcategory:
        context.user_data['subcategory_id'] = subcategory[0].id
        


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="complaintbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            #SETTINGS:[MessageHandler(filters.TEXT,settings)],
        },
        fallbacks=[CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,
        

    )
    application.add_handler(conv_handler)



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()