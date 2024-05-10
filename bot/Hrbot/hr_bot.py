import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')

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
from variables import text
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
from bot.Hrbot.bot_crud import crud
from bot.Hrbot.bot_services import transform_list
import database
from fastapi import Depends
languagees = {'1':'uz','2':'ru'}

load_dotenv()
manu_button = [['Задать вопрос❔','Отправить возражение📝'],['Часто задаваемые вопосы❓','Отправить предложение🧠'],['Настройки⚙️','О ботеℹ️'],['Chat']]


db = SessionLocal()
backend_location = 'app/'


#Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN_HR')
url = f"https://api.telegram.org/bot{BOTTOKEN}/sendMessage"
LANGUAGE,MANU,SPHERE,COMMENTS,QUESTIONS,LANGUPDATE,SETTINGS,SPHEREUPDATE,CHAT,CATEGORY= range(10)
persistence = PicklePersistence(filepath='hello.pickle')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = crud.get_user(db,update.message.from_user.id)
    if user:
        await update.message.reply_text(text['ru']['manu'],reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        context.user_data['lang'] = str(user.lang)
        context.user_data['sphere'] = user.sphere
        return MANU
    await update.message.reply_text(text['ru']['start'])
    await update.message.reply_text(text['ru']['lang'],reply_markup=ReplyKeyboardMarkup([['🇺🇿O`zbekcha','🇷🇺Русский']],resize_keyboard=True))
    return LANGUAGE



async def language(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == '🇺🇿O`zbekcha':
        context.user_data['lang'] = '1'
    else:
        context.user_data['lang'] = '2'
    spheres = crud.get_spheres(db)
    await update.message.reply_text(text[languagees[context.user_data['lang']]]['sphere'],reply_markup=ReplyKeyboardMarkup([[i.name for i in spheres]],resize_keyboard=True))
    return SPHERE


async def sphere(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:

    sphere = crud.get_spheres(db,update.message.text)
    context.user_data['sphere'] = sphere[0].id
    crud.create_user(db,id=update.message.from_user.id,lang=context.user_data['lang'],sphere=context.user_data['sphere'],name=update.message.from_user.first_name)
    await update.message.reply_text(text[languagees[context.user_data['lang']]]['success'],
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
    return MANU



async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == 'Задать вопрос❔':
        context.user_data['commentsphere'] = 1
        context.user_data['category'] = None
        await update.message.reply_text('Задайте вопрос',reply_markup=ReplyKeyboardMarkup([[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return COMMENTS

    elif update.message.text == 'Отправить возражение📝':
        context.user_data['commentsphere'] = 2
        data = crud.get_categories(db=db)
        buttons = transform_list(data,2,'name')

        buttons.append([text[languagees[context.user_data['lang']]]])

        await update.message.reply_text('Category',reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return CATEGORY

    elif update.message.text == 'Часто задаваемые вопосы❓':
        qeuestions = crud.get_questions(db=db,name=None,sphere=context.user_data['sphere']) 
        if questions:
            question_list = []
            for i in qeuestions:
                if context.user_data['lang'] == '1':
                    question_list.append([i.question_uz])
                else:
                    question_list.append([i.question_ru])
            question_list.append([[text[languagees[context.user_data['lang']]]['back']]])
            await update.message.reply_text('Часто задаваемые вопосы',reply_markup=ReplyKeyboardMarkup(question_list,resize_keyboard=True))
            return QUESTIONS
        else:
            await update.message.reply_text("Главная страница",
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
            return MANU
    elif update.message.text == 'Отправить предложение🧠':
        context.user_data['commentsphere'] = 3
        context.user_data['category'] =None
        await update.message.reply_text('Отправить предложение',reply_markup=ReplyKeyboardMarkup([[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return COMMENTS
    elif update.message.text == 'Настройки⚙️':
        #await update.message.reply_text('Настройки',reply_markup=ReplyKeyboardMarkup([['🇺🇿O`zbekcha','🇷🇺Русский']],resize_keyboard=True))
        await update.message.reply_text('Настройки',reply_markup=ReplyKeyboardMarkup([["Поменять сферу",'Изменить язык'],[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return SETTINGS
    elif update.message.text == 'О ботеℹ️':
        await update.message.reply_text(text[languagees[context.user_data['lang']]]['about'],
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        return MANU
    elif update.message.text == 'Chat':
        await update.message.reply_text('Чат',reply_markup=ReplyKeyboardMarkup([[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return CHAT




async def category(update: Update, context: ContextTypes.DEFAULT_TYPE, db=db) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text('Главная страница',
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        return MANU

    category_data = crud.get_categories(db=db,name=update.message.text)
    if category_data:
        context.user_data['category'] = category_data[0].id
        await update.message.reply_text('Введите текст',reply_markup=ReplyKeyboardMarkup([[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return COMMENTS
    else:
        data = crud.get_categories(db=db)
        reply_keyboard = transform_list(data,3,'name').append([text[languagees[context.user_data['lang']]]['back']])
        await update.message.reply_text('Категория не найдена',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return CATEGORY



async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text("Главная страница",
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        return MANU
    if update.message.text == 'Поменять сферу':
        spheres = crud.get_spheres(db)
        await update.message.reply_text(text[languagees[context.user_data['lang']]]['sphere'],reply_markup=ReplyKeyboardMarkup([[i.name for i in spheres]],resize_keyboard=True))
        return SPHEREUPDATE
    else:
        await update.message.reply_text('Язык',reply_markup=ReplyKeyboardMarkup([['🇺🇿O`zbekcha','🇷🇺Русский'],[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return LANGUPDATE
    
async def sphereupdate(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text('Настройки',reply_markup=ReplyKeyboardMarkup([["Поменять сферу",'Изменить язык'],[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return SETTINGS
    spheres = crud.get_spheres(db,name=update.message.text)
    context.user_data['sphere'] = spheres[0].id
    crud.update_user(db=db,id=update.message.from_user.id,lang=context.user_data['lang'],sphere=context.user_data['sphere'])
    await update.message.reply_text("Главная страница",
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
    return MANU


async def comments(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text("Главная страница",
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        return MANU
    crud.create_complaint(db=db,tel_id=update.message.from_user.id,complaint=update.message.text,sphere_id=context.user_data['sphere'],hrtype=context.user_data['commentsphere'],category=context.user_data['category'])
    # crud.create_request(database.session,int(context.user_data['commentsphere']),update.message.from_user.id)
    back = [[text[languagees[context.user_data['lang']]]['back']]]
    if context.user_data['commentsphere'] == 1:
        await update.message.reply_text(text[languagees[context.user_data['lang']]]['question_created'],
                                        reply_markup=ReplyKeyboardMarkup(back,resize_keyboard=True))
    elif context.user_data['commentsphere'] == 2:
        await update.message.reply_text(text[languagees[context.user_data['lang']]]['feedback_created'],
                                        reply_markup=ReplyKeyboardMarkup(back,resize_keyboard=True))

    elif context.user_data['commentsphere'] == 3:
        await update.message.reply_text(text[languagees[context.user_data['lang']]]['suggest_created'],
                                        reply_markup=ReplyKeyboardMarkup(back,resize_keyboard=True))
    return CHAT

async def langupdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text('Настройки',reply_markup=ReplyKeyboardMarkup([["Поменять сферу",'Изменить язык'],[text[languagees[context.user_data['lang']]]['back']]],resize_keyboard=True))
        return SETTINGS
    if update.message.text == '🇺🇿O`zbekcha':
        context.user_data['lang'] = str(1)
    else:
        context.user_data['lang'] = str(2)
    await update.message.reply_text("Главная страница",
                            reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
    return MANU
    

async def questions(update: Update, context: ContextTypes.DEFAULT_TYPE,db=db) -> int:
    if update.message.text == text[languagees[context.user_data['lang']]]['back']:
        await update.message.reply_text("Главная страница",
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
        return MANU
    question = crud.get_questions(db,name=update.message.text,sphere=context.user_data['sphere'])
    if question:
        await update.message.reply_text(question[0].answer_ru if context.user_data['lang'] == '2' else question[0].answer_uz,
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
    else:
        await update.message.reply_text('Вопрос не найден',
                                    reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
    
    return MANU


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    get_comlaint = crud.get_complaints(db=db,id=update.message.from_user.id)

    if update.message.text:
        input_text = update.message.text
        if input_text == '⬅️Назад':
            #data = crud.get_category_list(db=bot.session,department=4,sphere_status=4)
            #reply_keyboard = transform_list(data,3,'name')
            await update.message.reply_text('Главная страница',
                                        reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
            return MANU
        else:
            if '/start' != input_text or '':
                if get_comlaint:
                    if get_comlaint[0].status in [0,1]:
                        crud.create_message(db=db,hrcomplaint_id=get_comlaint[0].id,text=input_text,url=None)
                    else:
                        create_complaint = crud.create_complaint(db=db,tel_id=update.message.from_user.id,complaint=input_text,sphere_id=1)
                        crud.create_message(db=db,hrcomplaint_id=create_complaint.id,text=input_text,url=None)
            else:
                await update.message.reply_text('Главная страница',
                                                reply_markup=ReplyKeyboardMarkup(manu_button,resize_keyboard=True))
                return MANU
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
        with open(f"files/{file_name}",'wb') as f:
            f.write(file_content)
            f.close()
        if update.message.caption:
            text = update.message.caption
        else:
            text = None
        
        crud.create_message(db=db,text=text,hrcomplaint_id=get_comlaint[0].id,url=f"files/{file_name}")

    
    return CHAT



async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message

    if message.reply_to_message and message.reply_to_message.forward_from:
        chat_id = message.reply_to_message.forward_from.id
        text_message = update.message.text
        # Someone replied to a forwarded message
        # Perform your reaction here
        bot = context.bot
        print(text_message + "from hadle messages function")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="/app/bot/Hrbot/hrbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE:[MessageHandler(filters.TEXT,language)],
            SPHERE:[MessageHandler(filters.TEXT,sphere)],
            MANU:[MessageHandler(filters.TEXT,manu)],
            COMMENTS:[MessageHandler(filters.TEXT,comments)],
            QUESTIONS:[MessageHandler(filters.TEXT,questions)],
            LANGUPDATE:[MessageHandler(filters.TEXT,langupdate)],
            SPHEREUPDATE:[MessageHandler(filters.TEXT,sphereupdate)],
            SETTINGS:[MessageHandler(filters.TEXT,settings)],
            CHAT:[MessageHandler(filters.PHOTO | filters.Document.DOCX|filters.Document.IMAGE|filters.Document.PDF|filters.TEXT|filters.Document.MimeType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),chat)],
            CATEGORY:[MessageHandler(filters.TEXT,category)]
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