# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

reply_keyboard = [['/address', '/phone', '/help'],
                      ['/site', '/work_time', '/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-справочник. Я могу отправлять вам какую-то информацию!",
        reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.run_polling()

    application.run_polling()


if __name__ == '__main__':
    main()
