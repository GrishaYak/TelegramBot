import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
import os
from dotenv import load_dotenv
from Markups import get_markup
import asyncio
import psycopg
from constants import *
from usefull_functions import *
from Errors import *
import datetime
from db_connection import get_connection


async def start(update, context):
    connection = await get_connection()
    user = update.effective_user
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users where tg_username=%s", [user.username])
        if not cursor.fetchall():
            await update.message.reply_html(GREETINGS.format(nick=user.mention_html()), reply_markup=get_markup())
            await cursor.execute(f"INSERT INTO users values (%s);", [user.username])
            await connection.commit()
        await update.message.reply_text("Что хотите сделать?", reply_markup=get_markup(1))
        return 1


async def help_command(update, context):
    await update.message.reply_text(HELP_TXT)


async def add_consumption(update, context):
    await update.message.reply_text("Введите сумму расхода")
    context.user_data['sign'] = -1
    return 2


async def add_income(update, context):
    await update.message.reply_text("Введите сумму дохода", reply_markup=None)
    context.user_data['sign'] = 1
    return 2


async def add_alteration(update, context):
    try:
        context.user_data['sum'] = int(update.message.text)
        if context.user_data['sum'] >= (1 << 31):
            raise TooBig
        if context.user_data['sum'] < 0:
            raise IsNegative
    except TooBig:
        await update.message.reply_text("Пожалуйста, введите число поменьше!")
        return 2
    except IsNegative:
        await update.message.reply_text("Пожалуйста, введите положительное число!")
        return 2
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите только число!")
        return 2
    context.user_data['sum'] *= context.user_data['sign']
    username = update.effective_user.username
    categories = await get_categories(username)
    if categories:
        markup = ReplyKeyboardMarkup(sep_by_three(categories))
        await update.message.reply_text("Выберите категорию. Вы можете нажать на одну из тех, что вы уже создали, "
                                        "или просто написать новую", reply_markup=markup)
    else:
        await update.message.reply_text("К какой категории отнести это изменение?")
    return 3


async def add_alteration2(update, context):
    try:
        category_name = update.message.text
        if len(category_name) > 32:
            raise LenError
    except LenError:
        await update.message.reply_text("Название категории должно содержать не более 32 символов!")
        return 3
    username = update.effective_user.username
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute(f"SELECT id FROM categories WHERE name='{category_name}' AND user_id='{username}'")
        category_id = await cursor.fetchone()
        if category_id is None:
            await cursor.execute(f"INSERT INTO categories (name, user_id) VALUES {(category_name, username)}")
            await connection.commit()
        await cursor.execute(f"SELECT id FROM categories WHERE name='{category_name}' AND user_id='{username}'")
        category_id = await cursor.fetchone()
        context.user_data['category_id'] = category_id[0]
        await update.message.reply_text('Напишите краткое описание, или нажмите кнопку "Оставить пустым", '
                                        'чтобы не добавлять описание', reply_markup=get_markup(2))
    return 4


async def add_alteration_final(update, context):
    try:
        description = update.message.text
        if len(description) > 255:
            raise LenError
    except LenError:
        await update.message.reply_text("Название категории должно содержать не более 32 символов!")
        return 3
    if description == MT_DISCRIPTION:
        description = None
    connection = await get_connection()
    row = [update.effective_user.username, context.user_data['category_id'], context.user_data['sum'], description,
           datetime.date.today()]
    async with connection.cursor() as cursor:
        await cursor.execute(f"INSERT INTO alterations (user_id, category_id, summa, description, date) "
                             f"VALUES (%s, %s, %s, %s, %s)", row)
        await connection.commit()
        await update.message.reply_text("Записали!")
    return ConversationHandler.END


async def get_categories(username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute(f"SELECT name FROM categories WHERE user_id='{username}'")
        return [x[0] for x in await cursor.fetchall()]


async def checkout(update, context):
    pass


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
    delete_account_handler = CommandHandler("delete_me", delete_account)
    alteration_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration)
    alteration_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration2)
    alteration_handler_final = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_final)
    start_conv = ConversationHandler(
        entry_points=[start_handler],
        states={
            1: [consumption_handler, income_handler, checkout_handler, delete_account_handler],
            2: [alteration_handler],
            3: [alteration_handler2],
            4: [alteration_handler_final]
        },
        fallbacks=[escape_handler]
    )
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(start_conv)
    application.run_polling()


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
