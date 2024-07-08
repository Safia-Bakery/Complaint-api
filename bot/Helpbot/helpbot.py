#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    PicklePersistence
)

from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN_HELPDESK = os.environ.get('BOT_TOKEN_HELPDESK')

MESSAGES, FORWARDER = range(2)

forwarding_chat_id = '-1001429563019'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    await update.message.reply_text(
        """Здравствуйте! 🍰\nНапишите ваш вопрос и мы ответим Вам в ближайшее время. \n\n------------------------------------------------------\n\nSalom! 🍰\nSavolingizni yozing va biz sizga yaqin orada javob beramiz."""
    )

    return MESSAGES


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    await update.message.reply_text(
        """Благодарим за обратную связь, в скором времени свяжемся с вами😊\n\nRahmat savolingiz uchun, tez orada siz bilan bog'lanamiz😊"""
    )
    await context.bot.forward_message(chat_id=forwarding_chat_id, from_chat_id=update.message.from_user.id,
                                      message_id=update.message.id)
    return FORWARDER


async def forwarder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores tmhe selected gender and asks for a photo."""
    text_use = str(update.message.text)
    if '/start' != text_use:
        await context.bot.forward_message(chat_id=forwarding_chat_id, from_chat_id=update.message.from_user.id,
                                          message_id=update.message.id)
    else:
        await update.message.reply_text(
            """Здравствуйте! 🍰\nНапишите ваш вопрос и мы ответим Вам в ближайшее время.\n\n------------------------------------------------------\n\nSalom! 🍰\nSavolingizni yozing va biz sizga yaqin orada javob beramiz."""
        )
    return FORWARDER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text("Ko'rishguncha", reply_markup=ReplyKeyboardRemove()
                                    )

    return ConversationHandler.END


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message

    if message.reply_to_message and message.reply_to_message.forward_origin:
        chat_id = message.reply_to_message.forward_origin.sender_user.id
        text_message = update.message.text
        # Someone replied to a forwarded message
        # Perform your reaction here
        bot = context.bot
        await bot.send_message(chat_id=chat_id,text=text_message)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="helpbotcommunication")

    application = Application.builder().token(BOT_TOKEN_HELPDESK).persistence(persistence).build()
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MESSAGES: [MessageHandler(filters.ALL, messages)],
            FORWARDER: [MessageHandler(filters.ALL, forwarder)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    messagehanle = MessageHandler(filters.ALL, handle_messages)
    application.add_handler(conv_handler)
    application.add_handler(messagehanle)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
