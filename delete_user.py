from constants import ARE_YOU_SURE, KEY_WORD, ARE_NOT_SURE
from Markups import get_markup
from db import db


async def delete_user(update, context):
    await update.message.reply_text(ARE_YOU_SURE, reply_markup=get_markup(4))
    return 'are_you_sure'


async def delete_user2(update, context):
    answer = update.message.text
    if answer != KEY_WORD:
        await update.message.reply_text(ARE_NOT_SURE, reply_markup=get_markup(1))
        return 1
    await db.del_user(update.effective_user.username)
    await update.message.reply_text("Готово! Теперь мы не знакомы.", reply_markup=get_markup(3))
    return -1

