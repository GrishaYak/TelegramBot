from general.errors import TooBig, IsNegative, LenError
from general.constants import EMPTY_DESCRIPTION
from general.helpful_functions import sep_by_three
from datetime import date
from general.markups import get_markup
from telegram import ReplyKeyboardMarkup
from db import db


async def add_consumption(update, context):
    """Спрашивает сумму расхода, записывает что пользователь сохраняет именно расход, ведь далее диалог для записи и
    расходов и доходов будут обрабатывать одни и те же функции. Также он сразу обозначает знак суммы, ведь в БД
    разница между расходом и доходом заключается только в знаке суммы изменения."""
    await update.message.reply_text("Введите сумму расхода в рублях", reply_markup=get_markup(4))
    context.user_data['sign'] = -1
    context.user_data['type'] = 'расход'
    return 'add_alteration_sum'


async def add_income(update, context):
    """Спрашивает сумму дохода, записывает что пользователь сохраняет именно доход, ведь далее диалог для записи и
    расходов и доходов будут обрабатывать одни и те же функции. Также он сразу обозначает знак суммы, ведь в БД
    разница между расходом и доходом заключается только в знаке суммы изменения. """
    await update.message.reply_text("Введите сумму дохода в рублях", reply_markup=get_markup(4))
    context.user_data['sign'] = 1
    context.user_data['type'] = "доход"
    return 'add_alteration_sum'


async def process_sum(update, context):
    """Проверяет корректность введёной суммы. Если сообщение с суммой некоректно, возвращает строку, отсылающую
    пользователя на шаг назад. Иначе, не возвращает ничего"""
    try:
        context.user_data['sum'] = int(update.message.text)
        if context.user_data['sum'] >= (1 << 31):
            raise TooBig
        if context.user_data['sum'] <= 0:
            raise IsNegative
    except TooBig:
        await update.message.reply_text("Пожалуйста, введите число поменьше!", reply_markup=get_markup(4))
        return 'add_alteration_sum'
    except IsNegative:
        await update.message.reply_text("Пожалуйста, введите положительное число!", reply_markup=get_markup(4))
        return 'add_alteration_sum'
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите только число!", reply_markup=get_markup(4))
        return 'add_alteration_sum'


async def add_alteration_sum(update, context):
    """Получает сумму изменения из сообщения, отправляет её на проверку в функцию process_sum.
    Если что-то не так, возвращает пользователя на шаг назад.
    Записывает сумму в данные пользователя.
    Спрашивает у пользователя категорию изменения."""
    res = await process_sum(update, context)
    if res is not None:
        return res
    context.user_data['sum'] *= context.user_data['sign']
    username = update.effective_user.username

    keyboard = await db.get_categories_by_username(username)
    keyboard = [el[0] for el in keyboard]

    markup = ReplyKeyboardMarkup(sep_by_three(keyboard) + [['/escape']])
    if len(keyboard):
        await update.message.reply_text(f"Выберите категорию {context.user_data['type']}а. Вы можете нажать на одну из "
                                        f"тех, что вы уже создали, или просто написать новую", reply_markup=markup)
    else:
        await update.message.reply_text(f"Выберете категорию {context.user_data['type']}а.", reply_markup=markup)
    return 'add_alteration_category'


async def process_category(update):
    """Проверяет корректность введёного названия категории"""
    try:
        category_name = update.message.text
        if len(category_name) > 32:
            raise LenError
        return True, category_name
    except LenError:
        await update.message.reply_text("Название категории должно содержать не более 32 символов!")
        return False, 'add_alteration_category'


async def add_alteration_category(update, context):
    """Получает категорию изменения из сообщения, отправляет её на проверку в функцию process_category.
    Если что-то не так, возвращает пользователя на шаг назад.
    Записывает id категории в данные пользователя, заменяя одинарные кавычки на символ `.
    Предлагает пользователю задать описание изменению."""
    ok, category_name = await process_category(update)
    if not ok:
        return category_name

    category_name = category_name.replace("'", '`')  # Это нужно чтобы при записи категории в базу данных одинарная
    # кавычка не закрылась, вызвав при этом ошибку, или создав уеязвимость в виде SQL-инъекции
    username = update.effective_user.username
    category_id = await db.get_category_id(username, category_name)
    context.user_data['category_id'] = category_id[0]

    await update.message.reply_text(f'Напишите краткое описание этого {context.user_data["type"]}а, или нажмите '
                                    f'кнопку "Оставить пустым", чтобы не добавлять описание',
                                    reply_markup=get_markup(2))
    return 'add_alteration_description'


async def process_description(update):
    """Проверяет корректность введёного описания"""
    try:
        description = update.message.text
        if len(description) > 255:
            raise LenError
        return True, description
    except LenError:
        await update.message.reply_text("Описание должно содержать не более 255 символов!", reply_markup=get_markup(2))
        return False, 'add_alteration_description'


async def add_alteration_description(update, context):
    """Получает описание изменения из сообщения, отправляет её на проверку в функцию process_description.
    Если что-то не так, возвращает пользователя на шаг назад.
    Сохраняет изменение в БД, заменяя одинарные кавычки в описании на символ `."""
    ok, description = await process_description(update)

    if not ok:
        return description

    if description == EMPTY_DESCRIPTION:
        description = None
    else:
        description = description.replace("'", "`") # Это нужно чтобы при записи категории в базу данных одинарная
    # кавычка не закрылась, вызвав при этом ошибку, или создав уеязвимость в виде SQL-инъекции
    row = [update.effective_user.username, context.user_data['category_id'], context.user_data['sum'], description,
           date.today()]
    await db.add_alteration(*row)
    await update.message.reply_text("Записали!", reply_markup=get_markup(1))
    return 1
