from db import db
from general.markups import get_markup
from general.helpful_functions import process_numbers


async def delete_categories_which(update, context):
    """Спрашивает у пользователя номера категорий для удаления."""
    await update.message.reply_text("При удалении категории будут удалены все записи с этой категорией. "
                                    "Напишите номера категорий, которые вы хотите удалить. Например: 1,2,4-6")
    return 'delete_categories'


async def delete_categories(update, context):
    """Читает из чата номера категорий для удаления. Посредством функции process_numbers преобразует их в id категорий
    для удаления. Далее вызывает функцию для удаления категорий по id. В случае успеха, перенаправляет на начало
    диалога, иначе - на шаг назад"""
    numbers = update.message.text
    dicti = context.user_data['categories']
    ok, ids = await process_numbers(numbers, dicti, update)
    if not ok:
        return "delete_categories"

    await db.del_categories_by_ids(ids)
    await update.message.reply_text("Готово!", reply_markup=get_markup(1))
    return 1
