import sys
import os
from datetime import datetime
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')
from service import transform_list,validate_date,validate_only_date,send_file_telegram


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
    PicklePersistence, CallbackQueryHandler
)


from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
from queries import crud
load_dotenv()


backend_location = '/var/www/Complaint-api'

BOTTOKEN = os.environ.get('BOT_TOKEN_COMPLAINT')
MANU, BRANCH,SETTINGS,CATEGORY,SUBCATEGORY,NAME,PHONENUMBER,COMMENT,PHOTO,DATEPURCHASE,DATERETURN,VERIFY,BRANCHUPDATE,PRODUCTNAME= range(14)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    client = crud.get_client(id=user.id)
    if client and client.branch_id:
        context.user_data['branch_id'] = client.branch_id
        await update.message.reply_text(
            f"Главная страница",reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
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
            f"Главная страница",
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '⬅️Назад':
        await update.message.reply_text(
            'Главная страница',
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
            'Главная страница',
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU
    


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    category = crud.get_category(name=input_text)
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            f"Главная страница",
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
            'Введите название продукта',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PRODUCTNAME

async def productname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Введите номер клиента',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PHONENUMBER
    else:
        context.user_data['productname'] = input_text
        await update.message.reply_text(
            'Опишите причину жалобы, описание',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return COMMENT
    

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Введите название продукта',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return PRODUCTNAME
    else:
        context.user_data['comment'] = input_text
        await update.message.reply_text(
            'Прикрепите фото',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад', "➡️Далее"]],resize_keyboard=True)
        )
        context.user_data['file_url'] = []
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


        with open(f"{backend_location}/files/{file_name}", 'wb') as f:
            f.write(file_content)
            f.close()

        context.user_data['file_url'].append('files/'+file_name)
        await update.message.reply_text(
            "Фото добавлено",
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад', '➡️Далее']], resize_keyboard=True)
        )
        return PHOTO


    else:
        if update.message.text == '⬅️Назад':
            await update.message.reply_text(
                'Опишите причину жалобы, описание',
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад',]], resize_keyboard=True)
            )
            return COMMENT
        if update.message.text == '➡️Далее':
            await update.message.reply_text(
                'Дата покупки\nФормат: 23.04.2024 15:00',
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад',"➡️Пропустить"]], resize_keyboard=True)
            )
            return DATEPURCHASE
        else:
            await update.message.reply_text(
                "Прикрепите фото",
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад', '➡️Далее']], resize_keyboard=True)
            )
            return PHOTO

    

async def datepurchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Опишите причину жалобы, описание',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад']],resize_keyboard=True)
        )
        return COMMENT
    elif input_text == '➡️Пропустить':
        context.user_data['datepurchase'] = None
        await update.message.reply_text(
            "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад', "➡️Пропустить"]],resize_keyboard=True)
        )
        return DATERETURN

    else:
        is_valid = validate_date(input_text)
        if is_valid:

            context.user_data['datepurchase'] = input_text
            await update.message.reply_text(
                "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад',"➡️Пропустить"]],resize_keyboard=True)
            )
            return DATERETURN
        else:
            await update.message.reply_text(
            'Дата покупки\nФормат: 23.04.2024 15:00',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад',"➡️Пропустить"]],resize_keyboard=True)
            )
            return DATEPURCHASE
    


async def datereturn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if input_text == '⬅️Назад':
        await update.message.reply_text(
            'Дата покупки\nФормат: 23.04.2024 15:00',
            reply_markup=ReplyKeyboardMarkup([['⬅️Назад',"➡️Пропустить"]],resize_keyboard=True)
        )
        return DATEPURCHASE
    elif input_text == '➡️Пропустить':
        context.user_data['datereturn'] = None
        verify_text = f"Ваша заявка\nФилиал: {context.user_data['branch_name']}\nТип: : {context.user_data['category_name']}\nКатегория: {context.user_data['subcategory_name']}\nИмя: {context.user_data['name']}\nНомер: {context.user_data['phonenumber']}\nДата покупки: {context.user_data['datepurchase']}\nДата возврата: {context.user_data['datereturn']}\nКомментарий: {context.user_data['comment']}\nПродукт: {context.user_data['productname']}"
        await update.message.reply_text(
            verify_text,
            reply_markup=ReplyKeyboardMarkup([['Подтвердить','⬅️Назад']],resize_keyboard=True)
        )
        return VERIFY

    else:
        date_return = validate_only_date(input_text)
        if date_return:
            context.user_data['datereturn'] = input_text
            verify_text = f"Ваша заявка\nФилиал: {context.user_data['branch_name']}\nТип: : {context.user_data['category_name']}\nКатегория: {context.user_data['subcategory_name']}\nИмя: {context.user_data['name']}\nНомер: {context.user_data['phonenumber']}\nДата покупки: {context.user_data['datepurchase']}\nДата возврата: {context.user_data['datereturn']}\nКомментарий: {context.user_data['comment']}\nПродукт: {context.user_data['productname']}"
            await update.message.reply_text(
                verify_text,
                reply_markup=ReplyKeyboardMarkup([['Подтвердить','⬅️Назад']],resize_keyboard=True)
            )
            return VERIFY
        else:
            await update.message.reply_text(
                "Примерная дата отправки образцов (если есть)\nФормат: 23.04.2024",
                reply_markup=ReplyKeyboardMarkup([['⬅️Назад',"➡️Пропустить"]],resize_keyboard=True)
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
        if context.user_data['datepurchase'] == None:
            date_purchase_date = None
        else:
            date_purchase_date = datetime.strptime(context.user_data['datepurchase'], "%d.%m.%Y %H:%M")
        if context.user_data['datereturn'] == None:
            date_return_date = None
        else:
            date_return_date = datetime.strptime(context.user_data['datereturn']+" 10:00", "%d.%m.%Y %H:%M")
        create_complaint = crud.create_complaint(
                              branch_id=context.user_data['branch_id'],
                              subcategory_id=context.user_data['subcategory_id'],
                              name=context.user_data['name'],
                              phone_number=context.user_data['phonenumber'],
                              comment=context.user_data['comment'],
                              date_purchase=date_purchase_date,
                              datereturn=date_return_date,
                              product_name=context.user_data['productname']
                              )

        text_to_send = f"""
📁{create_complaint.subcategory.category.name}
🔘Категория: {create_complaint.subcategory.name}
🧑‍💼Имя: {create_complaint.client_name}
📞Номер: +{create_complaint.client_number}
📍Филиал: {create_complaint.branch.name}
🕘Дата покупки: {create_complaint.date_purchase}
🚛Дата отправки: {create_complaint.date_return}\n
💬Комментарии: {create_complaint.comment}\n
🍰Продукт: {create_complaint.product_name}
"""
        call_center_id = create_complaint.subcategory.country.callcenter_id

        #send to call center group
        message_sended = send_file_telegram(bot_token=BOTTOKEN,chat_id=call_center_id,file_path=None,caption=text_to_send)
        for i in context.user_data['file_url']:
            crud.create_file(complaint_id=create_complaint.id,file_name=i)
            send_file_telegram(bot_token=BOTTOKEN,chat_id=call_center_id,file_path= backend_location+'/'+i,caption=None,reply_to_message_id=message_sended['result']['message_id'])

        context.user_data['file_url'] = None

        await update.message.reply_text(
            "Ваша заявка принята. Id заявки: "+str(create_complaint.id),
            reply_markup=ReplyKeyboardMarkup([["Оформить жалобу", "Настройки"]],resize_keyboard=True)
        )
        return MANU



async def handle_callback_query(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    selected_option = int(query.data)
    message = query.message
    blank_reply_murkup = [[]]
    text_of_order = query.message.text
    requests_id = re.findall(r'\d+', text_of_order)[0]
    crud.get_user_with_telegram_id(telegram_id=query.from_user.id)
    crud.update_stamper_status(complaint_id=requests_id,user_id=query.id,status=selected_option)
    await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(blank_reply_murkup))










def main() -> None:
    """Run the bot."""
    callback_query_handler = CallbackQueryHandler(handle_callback_query)
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="complaintbotcommunication")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    application.add_handler(callback_query_handler)
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
            PHOTO:[MessageHandler(filters.ALL,photo)],
            DATEPURCHASE:[MessageHandler(filters.TEXT,datepurchase)],
            DATERETURN:[MessageHandler(filters.TEXT,datereturn)],
            VERIFY:[MessageHandler(filters.TEXT,verify)],
            BRANCHUPDATE:[MessageHandler(filters.TEXT,branch_update)],
            PRODUCTNAME:[MessageHandler(filters.TEXT,productname)]
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