import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
import os
from dotenv import load_dotenv
import asyncio
from constants import *
from alterations import *
from delete_alterations import delete_alteration, delete_alteration2
from checkout import checkout, checkout2


async def start(update, context):
    connection = await get_connection()
    user = update.effective_user
    context.user_data.clear()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE tg_username=%s", [user.username])
        if not await cursor.fetchall():
            await update.message.reply_html(GREETINGS.format(nick=user.mention_html()))
            await cursor.execute(f"INSERT INTO users VALUES (%s);", [user.username])
            await connection.commit()
        await update.message.reply_text("Что хотите сделать?", reply_markup=get_markup(1))
        return 1


async def help_command(update, context):
    await update.message.reply_text(HELP_TXT)


async def delete_account(update, context):
    pass


async def escape(update, context):
    await update.message.reply_text('Вы вернулись назад. Можете написать "/start", чтобы начать,'
                                    ' или "/help", если не знаете что делать', reply_markup=get_markup(3))
    return ConversationHandler.END


def main():
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    start_handler = CommandHandler("start", start)
    escape_handler = CommandHandler("escape", escape)
    consumption_handler = CommandHandler("consumption", add_consumption)
    income_handler = CommandHandler("income", add_income)
    checkout_handler = CommandHandler("checkout", checkout)
    checkout_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, checkout2)
    delete_account_handler = CommandHandler("delete_me", delete_account)
    alteration_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration)
    alteration_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration2)
    alteration_handler_final = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_final)
    delete_handler = CommandHandler("delete", delete_alteration)
    delete_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_alteration2)
    start_conv = ConversationHandler(
        entry_points=[start_handler],
        states={
            1: [consumption_handler, income_handler, checkout_handler, delete_account_handler],
            'alteration1': [alteration_handler],
            'alteration2': [alteration_handler2],
            'alteration3': [alteration_handler_final],
            'checkout': [checkout_handler2],
            'checkout_done': [checkout_handler2, delete_handler],
            'delete_alteration': [delete_handler2]
        },
        fallbacks=[escape_handler]
    )
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(start_conv)
    application.run_polling()


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                        filename='logs.txt')
    logger = logging.getLogger(__name__)
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
