from constants import CHECKOUT_TEXT, CHECKOUT_ALTERATION, CHECKOUT_ALTERATION_WOUT_DESCRIPTION, ALL_DATES
from Markups import get_markup
from Errors import TooManyWords
import datetime
from db import db


async def checkout_alteration(update, context):
    await update.message.reply_text(CHECKOUT_TEXT, reply_markup=get_markup(5))
    return 'checkout'


async def parse_dates(update, text):
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
        return 'checkout'
    except Exception:
        await update.message.reply_text("Неправильный формат!")
        return 'checkout'
    return dates


def add_alterations_to_user_data(res, context):

    for i in range(len(res)):
        res[i] = res[i][0]
    context.user_data['alts'] = {}
    for i in range(len(res)):
        context.user_data['alts'][i + 1] = res[i][0]
        res[i] = res[i][1:]
    return res


async def rows_to_text(update, alterations):
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


async def checkout_alteration2(update, context):
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
    return 'checkout_done'


async def show_all_alterations(update, context):
    username = update.effective_user.username
    res = add_alterations_to_user_data(await db.get_all_alterations(username), context)

    text = await rows_to_text(update, res)
    await update.message.reply_text(text)
    await update.message.reply_text("Вы можете ввести даты снова, или удалить какие-то из записей.",
                                    reply_markup=get_markup(6))
    return 'checkout_done'

