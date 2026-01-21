from constants import *
from db import db
from markups import get_markup


async def start(update, context):
    """Это начало диалога с пользователем. Если его нет в базе данных, то он будет туда занесён и при этом он получит
     сообщение-приветствие. После выполнения этой функции, пользователю становятся доступны все нужные команды"""
    user = update.effective_user
    context.user_data.clear()
    exists = await db.add_user_if_not_exists(user.username)
    if not exists:
        await update.message.reply_html(GREETINGS.format(nick=user.mention_html()))
    await update.message.reply_text("Что хотите сделать?", reply_markup=get_markup(1))
    return 1


async def help_command(update, context):
    """Эта функция просто выводит пользователю небольшую инструкцию по использованию бота."""
    await update.message.reply_text(HELP_TXT, reply_markup=get_markup(8))


async def escape(update, context):
    """Эта функция может быть вызвана в любой момент во время диалога, и она выводит пользователя из этого диалога
     в момент до написания команды start"""
    await update.message.reply_text('Вы вернулись назад. Напишите "/start", чтобы начать,', reply_markup=get_markup(3))
    return -1
