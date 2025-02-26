import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('.')
from bot.Hrbot.variables import buttons

import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    PicklePersistence

)


from variables import text
from dotenv import load_dotenv
from bot.Hrbot.bot_crud import crud
from bot.Hrbot.bot_services import transform_list

languagees = {'1': 'uz', '2': 'ru'}

load_dotenv()

backend_location = 'app/'

#Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN_HR')
url = f"https://api.telegram.org/bot{BOTTOKEN}/sendMessage"
LANGUAGE, MANU, SPHERE, COMMENTS, QUESTIONS, LANGUPDATE, SETTINGS, SPHEREUPDATE, CHAT, CATEGORY = range(10)


#persistence = PicklePersistence(filepath='/var/www/Complaint-api/bot/Hrbot/botpickle/hrbot/hello.pickle')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = crud.get_user(update.message.from_user.id)
    if user:
        context.user_data['lang'] = str(user.lang)
        context.user_data['sphere'] = user.sphere
        lang = languagees.get(context.user_data.get('lang'))
        await update.message.reply_text(text[lang]['manu'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))

        return MANU
    await update.message.reply_text(text['ru']['start'])
    await update.message.reply_text(text['ru']['lang'], reply_markup=ReplyKeyboardMarkup([['🇺🇿O`zbekcha', '🇷🇺Русский']],
                                                                                         resize_keyboard=True))
    return LANGUAGE


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '🇺🇿O`zbekcha':
        context.user_data['lang'] = '1'
    else:
        context.user_data['lang'] = '2'
    lang = languagees[context.user_data['lang']]
    spheres = crud.get_spheres()
    await update.message.reply_text(
        text[lang]['sphere'],
        reply_markup=ReplyKeyboardMarkup([[i.name if lang == 'ru' else i.name_uz for i in spheres]], resize_keyboard=True)
    )
    return SPHERE


async def sphere(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    sphere = crud.get_spheres(update.message.text)
    context.user_data['sphere'] = sphere[0].id
    lang = languagees[context.user_data['lang']]
    crud.create_user( id=update.message.from_user.id, lang=context.user_data['lang'],
                     sphere=context.user_data['sphere'], name=update.message.from_user.first_name)
    await update.message.reply_text(
        text[lang]['success'],
        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True)
    )
    return MANU


async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    input_text = update.message.text
    lang = languagees[context.user_data['lang']]
    if input_text == 'Задать вопрос❔' or input_text == 'Savol berish❔':
        context.user_data['commentsphere'] = 1
        context.user_data['category'] = None
        message_text = 'Задайте вопрос' if lang == 'ru' else 'Savolingizni yuboring'
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            [[text[lang]['back']]], resize_keyboard=True))
        return COMMENTS

    elif input_text == 'Отправить жалобу' or input_text == 'Shikoyat yuborish':
        context.user_data['commentsphere'] = 2
        data = crud.get_categories(hrsphere_id=context.user_data['sphere'])
        keyboard = transform_list(data, 2, 'name', lang)

        keyboard.append([text[lang]['back']])
        message_text = "Категория" if lang == 'ru' else "Kategoriya"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return CATEGORY

    elif input_text == 'Часто задаваемые вопосы❓' or input_text == 'Tez-tez beriladigan savollar❓':
        qeuestions = crud.get_questions(name=None, sphere=context.user_data['sphere'])
        if questions:
            question_list = []
            for i in qeuestions:
                if lang == 'uz':
                    question_list.append([i.question_uz])
                else:
                    question_list.append([i.question_ru])
            question_list.append([text[lang]['back']])

            message_text = "Часто задаваемые вопосы" if lang == 'ru' else "Tez-tez beriladigan savollar"
            await update.message.reply_text(message_text,
                                            reply_markup=ReplyKeyboardMarkup(question_list, resize_keyboard=True))
            return QUESTIONS
        else:
            await update.message.reply_text(text[lang]['home'],
                                            reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))
            return MANU

    elif input_text == 'Отправить предложение🧠' or input_text == 'Taklif yuborish🧠':
        context.user_data['commentsphere'] = 3
        context.user_data['category'] = None
        message_text = "Отправьте предложение" if lang == 'ru' else "Taklif yuboring"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            [[text[lang]['back']]], resize_keyboard=True))
        return COMMENTS

    elif input_text == 'Настройки⚙️' or input_text == 'Sozlamalar⚙️':
        message_text = "Настройки" if lang == 'ru' else "Sozlamalar"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            buttons[lang]["settings"],
            resize_keyboard=True))
        return SETTINGS

    elif input_text == 'О ботеℹ️' or input_text == 'Bot haqidaℹ️':
        await update.message.reply_text(text[lang]['about'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))
        return MANU

    elif input_text == 'Chat':
        message_text = "Чат" if lang == 'ru' else "Chat"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            [[text[lang]['back']]], resize_keyboard=True))
        return CHAT
    else:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))
        return MANU


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = languagees[context.user_data['lang']]

    if update.message.text == text[lang]['back']:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))
        return MANU

    category_data = crud.get_categories(name=update.message.text)
    if category_data:
        context.user_data['category'] = category_data[0].id
        message_text = "Введите текст" if lang == 'ru' else "Matn kiriting"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            [[text[lang]['back']]], resize_keyboard=True))
        return COMMENTS
    else:
        data = crud.get_categories( hrsphere_id=context.user_data['sphere'])
        reply_keyboard = transform_list(data, 3, 'name', lang).append([text[lang]['back']])
        message_text = "Категория не найдена" if lang == 'ru' else "Turkum topilmadi"
        await update.message.reply_text(message_text,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return CATEGORY


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE,) -> int:
    lang = languagees[context.user_data['lang']]
    if update.message.text == text[lang]['back']:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]["manu_button"], resize_keyboard=True))
        return MANU
    if update.message.text == 'Поменять сферу' or update.message.text == "Yo'nalishni o'zgartirish":
        spheres = crud.get_spheres()
        keyboard = transform_list(spheres, 2, 'name', lang)
        await update.message.reply_text(text[lang]['sphere'],
                                        reply_markup=ReplyKeyboardMarkup(keyboard,
                                                                         resize_keyboard=True))
        return SPHEREUPDATE
    else:
        message_text = "Выберите язык" if lang == 'ru' else "Tilni tanlang"
        await update.message.reply_text(message_text, reply_markup=ReplyKeyboardMarkup(
            [['🇺🇿O`zbekcha', '🇷🇺Русский'], [text[lang]['back']]],
            resize_keyboard=True))
        return LANGUPDATE


async def sphereupdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = languagees[context.user_data['lang']]
    if update.message.text == text[lang]['back']:
        message_text = "Настройки" if lang == 'ru' else "Sozlamalar"
        await update.message.reply_text(
            message_text,
            reply_markup=ReplyKeyboardMarkup(
                buttons[lang]["settings"],
                resize_keyboard=True
            )
        )
        return SETTINGS

    spheres = crud.get_spheres(name=update.message.text)
    context.user_data['sphere'] = spheres[0].id
    crud.update_user(id=update.message.from_user.id, lang=context.user_data['lang'],
                     sphere=context.user_data['sphere'])
    await update.message.reply_text(text[lang]['home'],
                                    reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
    return MANU


async def comments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = languagees[context.user_data['lang']]
    if update.message.text == text[lang]['back']:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
        return MANU
    query = crud.create_complaint( tel_id=update.message.from_user.id, complaint=update.message.text,
                                  sphere_id=context.user_data['sphere'], hrtype=context.user_data['commentsphere'],
                                  category=context.user_data['category'])
    crud.create_message(text=update.message.text, hrcomplaint_id=query.id, url=None)

    if context.user_data['commentsphere'] == 1:
        message_text = "Благодарим за обратную связь, в скором времени мы ответим вам😊" if lang == 'ru' \
            else "Rahmat savolingiz uchun, tez orada sizga javob beramiz😊"
        await update.message.reply_text(message_text,
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
    elif context.user_data['commentsphere'] == 2:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))

    elif context.user_data['commentsphere'] == 3:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
    return MANU


async def langupdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = languagees[context.user_data['lang']]
    if update.message.text == text[lang]['back']:
        message_text = "Настройки" if lang == 'ru' else "Sozlamalar"
        await update.message.reply_text(
            message_text,
            reply_markup=ReplyKeyboardMarkup(
                buttons[lang]["settings"],
                resize_keyboard=True
            )
        )
        return SETTINGS
    if update.message.text == '🇺🇿O`zbekcha':
        context.user_data['lang'] = str(1)
    else:
        context.user_data['lang'] = str(2)

    lang = languagees[context.user_data['lang']]
    crud.update_user(id=update.message.from_user.id, lang=context.user_data['lang'])
    await update.message.reply_text(text[lang]['home'],
                                    reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'],
                                                                     resize_keyboard=True))
    return MANU


async def questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = languagees[context.user_data['lang']]
    if update.message.text == text[lang]['back']:
        await update.message.reply_text(text[lang]['home'],
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'],
                                                                         resize_keyboard=True))
        return MANU
    question = crud.get_questions(name=update.message.text, sphere=context.user_data['sphere'])
    if question:
        await update.message.reply_text(
            question[0].answer_ru if lang == 'ru' else question[0].answer_uz,
            reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
    else:
        message_text = "Вопрос не найден" if lang == 'ru' else "Savol topilmadi"
        await update.message.reply_text(message_text,
                                        reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))

    return MANU


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE, text=text) -> int:
    """Stores the selected gender and asks for a photo."""
    get_comlaint = crud.get_complaints(id=update.message.from_user.id)
    lang = languagees[context.user_data['lang']]
    if update.message.text:
        input_text = update.message.text
        if input_text == text[lang]['back']:
            #data = crud.get_category_list(db=bot.session,department=4,sphere_status=4)
            #reply_keyboard = transform_list(data,3,'name')
            await update.message.reply_text(text[lang]['home'],
                                            reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
            return MANU
        else:
            if '/start' != input_text or '':
                if get_comlaint:
                    if get_comlaint[0].status in [0, 1]:
                        crud.create_message(hrcomplaint_id=get_comlaint[0].id, text=input_text, url=None)
                    else:
                        create_complaint = crud.create_complaint(tel_id=update.message.from_user.id,
                                                                 complaint=input_text, sphere_id=1)
                        crud.create_message(hrcomplaint_id=create_complaint.id, text=input_text, url=None)
            else:
                await update.message.reply_text(text[lang]['home'],
                                                reply_markup=ReplyKeyboardMarkup(buttons[lang]['manu_button'], resize_keyboard=True))
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
        with open(f"files/{file_name}", 'wb') as f:
            f.write(file_content)
            f.close()
        if update.message.caption:
            message_text = update.message.caption
        else:
            message_text = None

        crud.create_message(text=message_text, hrcomplaint_id=get_comlaint[0].id, url=f"files/{file_name}")

    return CHAT


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message

    if message.reply_to_message and message.reply_to_message.forward_origin:
        chat_id =  message.reply_to_message.forward_origin.sender_user.id
        text_message = update.message.text
        # Someone replied to a forwarded message
        # Perform your reaction here
        bot = context.bot


def main() -> None:
    """Run the bot."""

    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="hrbotcommunication")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT, language)],
            SPHERE: [MessageHandler(filters.TEXT, sphere)],
            MANU: [MessageHandler(filters.TEXT, manu)],
            COMMENTS: [MessageHandler(filters.TEXT, comments)],
            QUESTIONS: [MessageHandler(filters.TEXT, questions)],
            LANGUPDATE: [MessageHandler(filters.TEXT, langupdate)],
            SPHEREUPDATE: [MessageHandler(filters.TEXT, sphereupdate)],
            SETTINGS: [MessageHandler(filters.TEXT, settings)],
            CHAT: [MessageHandler(filters.PHOTO |
                                  filters.Document.DOCX |
                                  filters.Document.IMAGE |
                                  filters.Document.PDF |
                                  filters.TEXT |
                                  filters.Document.MimeType(
                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), chat)],
            CATEGORY: [MessageHandler(filters.TEXT, category)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,
    )
    messagehandle = MessageHandler(filters.ALL, handle_messages)
    application.add_handler(conv_handler)

    application.add_handler(messagehandle)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
