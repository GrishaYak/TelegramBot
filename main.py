import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
import os
from dotenv import load_dotenv
import asyncio
from constants import *
from alterations import *
from delete_alterations import delete_alteration, delete_alteration2
from checkout_alteration import checkout_alteration, checkout_alteration2
from delete_user import delete_user, delete_user2
from checkout_categories import checkout_categories
from delete_categories import delete_categories_which, delete_categories


async def start(update, context):
    user = update.effective_user
    context.user_data.clear()
    exists = await db.add_user_if_not_exists(user.username)
    if not exists:
        await update.message.reply_html(GREETINGS.format(nick=user.mention_html()))
    await update.message.reply_text("Что хотите сделать?", reply_markup=get_markup(1))
    return 1


async def help_command(update, context):
    await update.message.reply_text(HELP_TXT)


async def escape(update, context):
    await update.message.reply_text('Вы вернулись назад. Можете написать "/start", чтобы начать,'
                                    ' или "/help", если не знаете что делать', reply_markup=get_markup(3))
    return ConversationHandler.END


def main():
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    start_handler = CommandHandler("start", start)

    escape_handler = CommandHandler("escape", escape)

    checkout_alteration_handler = CommandHandler("checkout", checkout_alteration)
    checkout_alteration_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, checkout_alteration2)

    delete_user_handler = CommandHandler("delete_me", delete_user)
    delete_user_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_user2)

    consumption_handler = CommandHandler("consumption", add_consumption)
    income_handler = CommandHandler("income", add_income)
    alteration_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration)
    alteration_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration2)
    alteration_handler_final = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_final)

    delete_alterations_handler = CommandHandler("delete", delete_alteration)
    delete_alterations_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_alteration2)

    checkout_categories_handler = CommandHandler('checkout_categories', checkout_categories)

    delete_categories_which_handler = CommandHandler('delete_categories', delete_categories_which)
    delete_categories_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_categories)

    start_conv = ConversationHandler(
        entry_points=[start_handler],
        states={
            1: [consumption_handler, income_handler, checkout_alteration_handler, delete_user_handler,
                checkout_categories_handler],
            'add_alteration': [alteration_handler],
            'add_alteration2': [alteration_handler2],
            'add_alteration3': [alteration_handler_final],
            'checkout': [checkout_alteration_handler2],
            'checkout_done': [checkout_alteration_handler2, delete_alterations_handler],
            'delete_alteration': [delete_alterations_handler2],
            'are_you_sure': [delete_user_handler2],
            'delete_categories_which': [delete_categories_which_handler],
            'delete_categories': [delete_categories_handler]
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
