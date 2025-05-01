# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

reply_keyboard = [['/start', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")
    return 1


async def first_response(update, context):
    locality = update.message.text
    await update.message.reply_text(
        f"Какая погода в городе {locality}?")
    return 2


async def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    await update.message.reply_text("Какие цифры написаны на обороте вашей банковской карты?")
    return 3


async def bye(update, context):
    logger.info(update.message.text)
    await update.message.reply_text("Всего доброго!")


async def stop(update, context):
    logger.info(update.message.text)
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def help_command(update, context):
    keyboard = [['/start']]
    markup1 = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Я абсолютно безобидный бот. Хочешь со мной поболтать? Тогда напиши /start", reply_markup=markup1)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, bye)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
