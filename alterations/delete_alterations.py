from db import db
from general.markups import get_markup
from general.helpful_functions import process_numbers


async def delete_alteration(update, context):
    """Спрашивает у пользователя номера записей(изменений) для удаления."""
    await update.message.reply_text("Введите номера записей, которые вы хотите удалить. Например: 1,2,4-6",
                                    reply_markup=get_markup(4))
    return 'delete_alteration'


async def delete_alteration2(update, context):
    """Читает из чата номера категорий для удаления. Посредством функции process_numbers преобразует их в id категорий
   для удаления. Далее вызывает функцию для удаления категорий по id. В случае успеха, перенаправляет на начало
   диалога, иначе - на шаг назад"""
    numbers = update.message.text
    dicti = context.user_data['alts']
    ok, ids = await process_numbers(numbers, dicti, update)
    if not ok:
        return "delete_alteration"

    await db.del_alterations_by_ids(ids)
    await update.message.reply_text("Готово!", reply_markup=get_markup(1))
    return 1


