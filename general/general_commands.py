from constants import *
from db import db
from markups import get_markup


async def start(update, context):
    user = update.effective_user
    context.user_data.clear()
    exists = await db.add_user_if_not_exists(user.username)
    if not exists:
        await update.message.reply_html(GREETINGS.format(nick=user.mention_html()))
    await update.message.reply_text("Что хотите сделать?", reply_markup=get_markup(1))
    return 1


async def help_command(update, context):
    await update.message.reply_text(HELP_TXT, reply_markup=get_markup(8))


async def escape(update, context):
    await update.message.reply_text('Вы вернулись назад. Можете написать "/start", чтобы начать,'
                                    ' или "/help", если не знаете что делать', reply_markup=get_markup(3))
    return -1
