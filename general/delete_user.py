from general.constants import ARE_YOU_SURE, KEY_WORD, ARE_NOT_SURE
from general.markups import get_markup
from db import db


async def delete_user_question(update, context):
    """Эта функция спрашивает пользователя уверен ли он, что хочет удалить себя из бд,
    и передаёт его следующему обработчику."""
    await update.message.reply_text(ARE_YOU_SURE, reply_markup=get_markup(4))
    return 'delete_user'


async def delete_user(update, context):
    """Эта функция удаляет все записи и категории, принадлежащие пользователю, а также его самого,
    если он правильно введёт ключевое слово."""
    answer = update.message.text
    if answer != KEY_WORD:
        await update.message.reply_text(ARE_NOT_SURE, reply_markup=get_markup(1))
        return 1
    await db.del_user(update.effective_user.username)
    await update.message.reply_text("Готово! Теперь мы не знакомы.", reply_markup=get_markup(3))
    return -1

