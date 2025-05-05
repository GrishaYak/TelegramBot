from general.constants import CHECKOUT_TEXT, CHECKOUT_ALTERATION, CHECKOUT_ALTERATION_WOUT_DESCRIPTION, ALL_DATES
from general.markups import get_markup
from general.errors import TooManyWords
import datetime
from db import db


async def checkout_alteration_question(update, context):
    """Спрашивает какие записи интересут пользователя."""
    await update.message.reply_text(CHECKOUT_TEXT, reply_markup=get_markup(5))
    return 'checkout_alteration'


async def parse_dates(update, text):
    """Проверяет корректность введёных дат/введёной даты"""
    try:
        dates = text.split()
        if len(dates) > 2:
            raise TooManyWords
        dates = [el.split('.') for el in dates]
        if any([len(el) != 3 for el in dates]):
            raise TypeError
        dates = [datetime.date(*[int(el) for el in dat[::-1]]) for dat in dates]
    except TooManyWords:
        await update.message.reply_text("Нужно написать не более двух дат!")
        return 'checkout_alteration'
    except Exception:
        await update.message.reply_text("Неправильный формат!")
        return 'checkout_alteration'
    return dates


async def checkout_alteration(update, context):
    f"""Читает из сообщения дат(у/ы)/'{ALL_DATES}' - ключевое слово, обозначающее, что пользователь хочет получить все
     свои записи. Проверяет корректность дат, если нужно, функцией parse_dates.
    Выводит пользователю все его записи за нужный промежуток времени, создаёт словарь в user_data в котором по ключу 
    порядкового номера изменений хранятся id этих изменений
    Предлагает пользователю посмотреть записи за другие даты или удалить даты из данного ему списка"""
    text = update.message.text
    username = update.effective_user.username

    if text == ALL_DATES:
        return await show_all_alterations(update, context)

    dates = await parse_dates(update, text)
    if isinstance(dates, str):
        return dates

    alterations = add_alterations_to_user_data(await db.get_alterations_by_date(dates, username), context)

    text = await rows_to_text(update, alterations)

    await update.message.reply_text(text)
    await update.message.reply_text("Вы можете ввести даты снова, или удалить какие-то из записей.",
                                    reply_markup=get_markup(6))
    return 'checkout_alteration_done'


def add_alterations_to_user_data(alterations, context):
    """Сохраняет id изменений в данные пользователя, возвращает те же изменения, но убирает у каждого изменения
     id изменения в начале"""
    for i in range(len(alterations)):
        alterations[i] = alterations[i][0]
    context.user_data['alts'] = {}
    for i in range(len(alterations)):
        context.user_data['alts'][i + 1] = alterations[i][0]
        alterations[i] = alterations[i][1:]
    return alterations


async def rows_to_text(update, alterations):
    """Переводит изменения, записанные в двумерный массив в текс, который будет отправлен пользователю.
    В массиве alterations нужно хранить следующие данные в следующем порядке:
    сумма изменения;
    id категории изменения;
    описание изменения;
    дата изменения.
    """
    text = ''
    for i in range(len(alterations)):
        alt = list(alterations[i])
        alt[0] = int(alt[0])
        if alt[0] < 0:
            alt[0] *= -1
            typ = "расход"
        else:
            typ = "доход"

        category_name = await db.get_category_name_by_id(alt[1])
        category_name = category_name[0]
        description = alt[2]
        dat = '.'.join(list(reversed(alt[3].split('-'))))
        if description is None:
            text += CHECKOUT_ALTERATION_WOUT_DESCRIPTION.format(num=i + 1, type=typ.capitalize(), date=dat,
                                                                category=category_name, summa=alt[0])
            continue
        text += CHECKOUT_ALTERATION.format(num=i + 1, type=typ.capitalize(), date=dat, category=category_name,
                                           summa=alt[0], description=description)
    if not text:
        text = "У вас пока что ничего не записано."
    return text


async def show_all_alterations(update, context):
    """Показывает пользователю все его записи.
    Создаёт словарь в user_data в котором по ключу порядкового номера изменений хранятся id этих изменений.
    Предлагает пользователю посмотреть записи за другие даты или удалить даты из данного ему списка"""
    username = update.effective_user.username
    res = add_alterations_to_user_data(await db.get_all_alterations(username), context)

    text = await rows_to_text(update, res)
    await update.message.reply_text(text)
    await update.message.reply_text("Вы можете ввести даты снова, или удалить какие-то из записей.",
                                    reply_markup=get_markup(6))
    return 'checkout_alteration_done'

