from db_connection import get_connection
from Errors import NotInList
from db import db
from Markups import get_markup


async def delete_alteration(update, context):
    await update.message.reply_text("Введите номера записей, которые вы хотите удалить. Например: 1,2,4-6")
    return 'delete_alteration'


async def delete_alteration2(update, context):
    text = update.message.text.split(',')
    ids = []
    dicti = context.user_data['alts']
    for el in text:
        if el.isdigit():
            try:
                if int(el) not in dicti:
                    raise NotInList
                ids.append(dicti[int(el)])
                continue
            except NotInList:
                await update.message.reply_text("Одного из номеров не было в списке!")
                return 'delete_alteration'
        if len(el.split('-')) != 2:
            await update.message.reply_text("Неправильный формат!")
            return 'delete_alteration'
        a, b = [int(i) for i in el.split('-')]
        try:
            ids += get_ids(list(range(a, b + 1)), dicti)
        except NotInList:
            await update.message.reply_text("Одного из номеров не было в списке!")
            return 'delete_alteration'
    await del_by_ids(ids)
    await update.message.reply_text("Готово!", reply_markup=get_markup(1))
    return 1


async def del_by_ids(ids):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(ids) > 1:
            await cursor.execute(f"DELETE FROM alterations WHERE id IN {tuple(ids)}")
        else:
            await cursor.execute("DELETE FROM alterations WHERE id=%s", ids)
        await connection.commit()


def get_ids(arr, dicti):
    res = []
    for el in arr:
        if el not in dicti:
            raise NotInList
        res.append(dicti[el])
    return res
