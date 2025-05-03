import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardRemove
import os
from dotenv import load_dotenv
from Markups import get_markup
import asyncio
import psycopg2
from constants import *

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

CONNECTION = psycopg2.connect(database="FinancesBot", user="postgres", password="123")
CURSOR = CONNECTION.cursor()


async def start(update, context):
    user = update.effective_user
    CURSOR.execute(f"SELECT * FROM users where tg_username='{user.username}'")
    if not CURSOR.fetchall():
        await update.message.reply_html(
            rf'''Привет {user.mention_html()}!
Я бот для записи изменений на вашем финансовом счету. Приятно познакомиться!''', reply_markup=get_markup())
        CURSOR.execute(f"INSERT INTO users values ('{user.username}');")
        CONNECTION.commit()
        print("added", user.username)
    await update.message.reply_text("Вы можете добавить расход, написав */consumption*, добавить доход, "
                                    "написав */income*, или "
                                    "посмотреть, и, возможно, редактировать изменения на счету, написав */check*."
                                    "Также вы можете удалить все данные о себе, если напишите */delete_me*",
                                    reply_markup=get_markup(1))
    return 1


async def help_command(update, context):
    await update.message.reply_text(HELP_TXT)


async def add_consumption(update, context):
    pass


async def add_income(update, context):
    pass


async def checkout(update, context):
    pass


async def delete_account(update, context):
    pass


def main():
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    start_handler = CommandHandler("start", start)
    consumption_handler = CommandHandler("consumption", add_consumption)
    income_handler = CommandHandler("income", add_income)
    checkout_handler = CommandHandler("checkout", checkout)
    delete_account_handler = CommandHandler("delete_me", delete_account)
    start_conv = ConversationHandler(
        entry_points=[start_handler],
        states={
            1: [consumption_handler, income_handler, checkout_handler, delete_account_handler]
        },
        fallbacks=[start_handler]
    )
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(start_conv)
    application.run_polling()


if __name__ == '__main__':
    main()
