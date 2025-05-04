from Errors import TooBig, IsNegative, LenError
from db_connection import get_connection
from constants import MT_DISCRIPTION
from usefull_functions import sep_by_three
from datetime import date
from Markups import get_markup
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


async def add_consumption(update, context):
    await update.message.reply_text("Введите сумму расхода")
    context.user_data['sign'] = -1
    context.user_data['type'] = 'расход'
    return 2


async def add_income(update, context):
    await update.message.reply_text("Введите сумму дохода", reply_markup=None)
    context.user_data['sign'] = 1
    context.user_data['type'] = "доход"
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
        await update.message.reply_text(f"Выберите категорию {context.user_data['type']}а. Вы можете нажать на одну из "
                                        f"тех, что вы уже создали, или просто написать новую", reply_markup=markup)
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

        await update.message.reply_text(f'Напишите краткое описание этого {context.user_data["type"]}а, или нажмите '
                                        f'кнопку "Оставить пустым", чтобы не добавлять описание',
                                        reply_markup=get_markup(2))
    return 4


async def add_alteration_final(update, context):
    try:
        description = update.message.text
        if len(description) > 255:
            raise LenError
    except LenError:
        await update.message.reply_text("Описание должно содержать не более 255 символов!")
        return 3
    if description == MT_DISCRIPTION:
        description = None
    else:
        description = description.replace("'", "`")
    connection = await get_connection()
    row = [update.effective_user.username, context.user_data['category_id'], context.user_data['sum'], description,
           date.today()]
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
