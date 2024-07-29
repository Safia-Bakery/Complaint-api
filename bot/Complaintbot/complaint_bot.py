import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')
from service import transform_list,validate_date,validate_only_date


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
    CallbackQueryHandler,
    PicklePersistence
)

from database import SessionLocal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
from queries import crud
load_dotenv()


backend_location = '/var/www/Complaint-api'

BOTTOKEN = os.environ.get('BOT_TOKEN_COMPLAINT')
persistence = PicklePersistence(filepath='complaint.pickle')
MANU, BRANCH,SETTINGS,CATEGORY,SUBCATEGORY,NAME,PHONENUMBER,COMMENT,PHOTO,DATEPURCHASE,DATERETURN,VERIFY,BRANCHUPDATE= range(13)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    client = crud.get_client(id=user.id)
    if client and client.branch_id:
        context.user_data['branch_id'] = client.branch_id
        await update.message.reply_text(
            f"Manu",reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        current_branch = crud.get_branchs(id=client.branch_id)
        context.user_data['branch_name'] = current_branch.name
        return MANU
    elif not client:
        await update.message.reply_text(
            f"Привет. Это корпоративный телеграм бот для оформления жалоб. Пожалуйста введите пароль который вы получили от системного администратора",
        )
        return BRANCH
    elif not client.branch_id:
        await update.message.reply_text(
            'Введите пароль',
            reply_markup=ReplyKeyboardRemove()
        )
        return BRANCHUPDATE
    
    

async def branch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    input_data = update.message.text    
    branch_name = crud.get_branchs(password=input_data)
    if branch_name:
        crud.create_client(name=update.message.from_user.first_name,id = update.message.from_user.id,branch_id=branch_name.id)
        context.user_data['branch_name'] = branch_name.name
        context.user_data['branch_id'] = branch_name.id
        await update.message.reply_text(
            f"Ваш филиал - {branch_name.name}",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    else:
        await update.message.reply_text(
            f"Пароль не верный. Попробуйте еще раз",
        )
        return BRANCH



async def branch_update(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    input_text = update.message.text
    branch_name = crud.get_branchs(password=input_text)
    if branch_name: 
        crud.update_client(id=update.message.from_user.id,branch_id=branch_name.id)
        await update.message.reply_text(
            f"Пожалуйста введите пароль который вы получили от системного администратора",
            reply_markup=ReplyKeyboardMarkup([['Branch','⬅️Назад']],resize_keyboard=True)
        )
        return  SETTINGS
    else:
        await update.message.reply_text(
            f"Пароль не верный. Попробуйте еще раз",
        )
        return BRANCHUPDATE




async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    input_data = update.message.text
    if input_data == "Оформить жалобу":
        categories = crud.get_category()
        buttons = transform_list(categories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
        'Выбрать тип',
        reply_markup=reply_markup
    )
        return CATEGORY
    elif input_data == "Настройки":
        await update.message.reply_text(
            f"Пожалуйста введите пароль который вы получили от системного администратора",
            reply_markup=ReplyKeyboardMarkup([['Branch','⬅️Назад']],resize_keyboard=True)
        )
        return  SETTINGS
    else:
        await update.message.reply_text(
            f"Manu",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '⬅️Назад':
        await update.message.reply_text(
            'Manu',
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU

    elif text == 'Branch':
        await update.message.reply_text(
            'Введите пароль',
            reply_markup=ReplyKeyboardRemove()
        )
        return BRANCHUPDATE
    else:
        await update.message.reply_text(
            'Manu',
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    category = crud.get_category(name=input_text)
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            f"Manu",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    if category:
        context.user_data['category_id'] = category[0].id
        context.user_data['category_name'] = category[0].name
        subcategories = category[0].subcategory
        buttons = transform_list(subcategories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
            'Выберите категорию',
            reply_markup=reply_markup
        )
        return SUBCATEGORY
    else:

        categories = crud.get_category()
        buttons = transform_list(categories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
        'Выбрать тип',
        reply_markup=reply_markup)
        return CATEGORY
    

async def subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    subcategory = crud.get_subcategory(name=data,category_id=context.user_data['category_id'])
    
    if data == '⬅️Назад':
        categories = crud.get_category()
        buttons = transform_list(categories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
        'Выберите категорию жалобы',
        reply_markup=reply_markup)
        return CATEGORY
    if subcategory:
        context.user_data['subcategory_id'] = subcategory[0].id
        context.user_data['subcategory_name'] = subcategory[0].name
        await update.message.reply_text(
            'Введите имя клиента',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return NAME
    else:
        subcategories = crud.get_subcategory(category_id=context.user_data['category_id'])
        buttons = transform_list(subcategories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
            'Выбрать тип',
            reply_markup=reply_markup
        )
        return SUBCATEGORY


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        subcategories = crud.get_subcategory(category_id=context.user_data['category_id'])
        buttons = transform_list(subcategories,2,'name')
        reply_markup = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        await update.message.reply_text(
            'Выберите категорию',
            reply_markup=reply_markup
        )
        return SUBCATEGORY
    else:
        context.user_data['name'] = input_text
        await update.message.reply_text(
            'Введите номер клиента',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PHONENUMBER
    


async def phonenumber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Введите имя клиента',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return NAME
    else:
        context.user_data['phonenumber'] = input_text
        await update.message.reply_text(
            'Введите комментарий',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return COMMENT
    

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Введите номер клиента',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PHONENUMBER
    else:
        context.user_data['comment'] = input_text
        await update.message.reply_text(
            'Прикрепите фото',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PHOTO
    

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        if update.message.document:
        #context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)
            file_content = await new_file.download_as_bytearray()
            #files_open = {'files':file_content}
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()
            #files_open = {'files':file_content}
        with open(f"{backend_location}/files/{file_name}",'wb') as f:
            f.write(file_content)
            f.close()
        context.user_data['file_url'] = f"files/{file_name}"
        await update.message.reply_text(
            'Дата покупки\nФормат: 23.04.2024 15:00',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return DATEPURCHASE
    else:
        if update.message.text == '⬅️Назад':
            await update.message.reply_text(
                'Введите комментарий',
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад']], resize_keyboard=True)
            )
            return COMMENT
        await update.message.reply_text(
            'Прикрепите фото',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PHOTO
    

async def datepurchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Введите комментарий',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return COMMENT
    else:
        is_valid = validate_date(input_text)
        if is_valid:

            context.user_data['datepurchase'] = input_text
            await update.message.reply_text(
                "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
            )
            return DATERETURN
        else:
            await update.message.reply_text(
            'Дата покупки\nФормат: 23.04.2024 15:00',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
            )
            return DATEPURCHASE
    


async def datereturn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Дата покупки\nФормат: 23.04.2024 15:00',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return DATEPURCHASE
    else:
        date_return = validate_only_date(input_text)
        if date_return:
            context.user_data['datereturn'] = input_text
            verify_text = f"Ваша заявка\nФилиал: {context.user_data['branch_name']}\nТип: : {context.user_data['category_name']}\nКатегория: {context.user_data['subcategory_name']}\nИмя: {context.user_data['name']}\nНомер: {context.user_data['phonenumber']}\nДата покупки: {context.user_data['datepurchase']}\nДата возврата: {context.user_data['datereturn']}\nКомментарий: {context.user_data['comment']}"
            await update.message.reply_text(
                verify_text,
                reply_markup=ReplyKeyboardMarkup([['Подтвердить','⬅️Назад']],resize_keyboard=True)
            )
            return VERIFY
        else:
            await update.message.reply_text(
                "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
            )
            return DATERETURN
    

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",   
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return DATERETURN
    else:
        
        date_purchase_date = datetime.strptime(context.user_data['datepurchase'], "%d.%m.%Y %H:%M")
        date_return_date = datetime.strptime(context.user_data['datereturn']+" 10:00", "%d.%m.%Y %H:%M")
        created_order = crud.create_complaint(
                              branch_id=context.user_data['branch_id'],
                              subcategory_id=context.user_data['subcategory_id'],
                              name=context.user_data['name'],
                              phone_number=context.user_data['phonenumber'],
                              comment=context.user_data['comment'],
                              date_purchase=date_purchase_date,
                              datereturn=date_return_date)

        create_file = crud.create_file(complaint_id=created_order.id,file_name=context.user_data['file_url'])
        await update.message.reply_text(
            "Ваша заявка принята. Id заявки: "+str(created_order.id),
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    

    

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message

    if message.reply_to_message and message.reply_to_message.forward_from:
        chat_id = message.reply_to_message.forward_from.id
        text_message = update.message.text
        # Someone replied to a forwarded message
        # Perform your reaction here
        bot = context.bot





def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="complaintbotcommunication")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            #SETTINGS:[MessageHandler(filters.TEXT,settings)],
            BRANCH:[MessageHandler(filters.TEXT,branch)],
            MANU:[MessageHandler(filters.TEXT,manu)],
            SETTINGS:[MessageHandler(filters.TEXT,settings)],
            CATEGORY:[MessageHandler(filters.TEXT,category)],
            SUBCATEGORY:[MessageHandler(filters.TEXT,subcategory)],
            NAME:[MessageHandler(filters.TEXT,name)],
            PHONENUMBER:[MessageHandler(filters.TEXT,phonenumber)],
            COMMENT:[MessageHandler(filters.TEXT,comment)],
            PHOTO:[MessageHandler(filters.PHOTO | filters.Document.DOCX|filters.Document.IMAGE|filters.Document.PDF|filters.TEXT|filters.Document.MimeType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),photo)],
            DATEPURCHASE:[MessageHandler(filters.TEXT,datepurchase)],
            DATERETURN:[MessageHandler(filters.TEXT,datereturn)],
            VERIFY:[MessageHandler(filters.TEXT,verify)],
            BRANCHUPDATE:[MessageHandler(filters.TEXT,branch_update)]

        },
        fallbacks=[CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,
        

    )
    messagehandle = MessageHandler(filters.ALL,handle_messages)
    application.add_handler(conv_handler)
    application.add_handler(messagehandle)



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()