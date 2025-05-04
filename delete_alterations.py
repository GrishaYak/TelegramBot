from db import db
from Markups import get_markup
from usefull_functions import process_numbers


async def delete_alteration(update, context):
    await update.message.reply_text("Введите номера записей, которые вы хотите удалить. Например: 1,2,4-6",
                                    reply_markup=get_markup(4))
    return 'delete_alteration'


async def delete_alteration2(update, context):
    numbers = update.message.text.split(',')
    dicti = context.user_data['alts']
    ok, ids = await process_numbers(numbers, dicti, update)
    if not ok:
        return "delete_alteration"

    await db.del_alterations_by_ids(ids)
    await update.message.reply_text("Готово!", reply_markup=get_markup(1))
    return 1


