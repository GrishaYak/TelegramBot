from db import db
from general.markups import get_markup


async def checkout_categories(update, context):
    """Выводит все категории пользователя, спрашивает что он хочет делать дальше."""
    username = update.effective_user.username
    await update.message.reply_text('За вами числятся следующие категории: ')
    categories = await db.get_categories_by_username(username)
    ids = []
    for el in categories:
        i = await db.get_category_id(username, el[0])
        # выше el[0] потому, что в categories лежал картеж вида (('categ',), ('categ2',)...)
        ids.append(i[0])   # Здесь i[0] по схожим причинам: cursor.fetchone() и cursor.fetchall() зачем-то оборачивают
        #                   всё в лишний слой картежей
    reply = ""
    context.user_data["categories"] = {}  # Здесь
    for i in range(len(categories)):
        reply += f'{i + 1}) "{categories[i][0]}"\n'
        context.user_data["categories"][i + 1] = str(ids[i])  # и здесь я сохраняю id категории как значение по ключу
        #    её порядкового номера, мне это пригодится, если пользователь захочет удалить какие-то из своих категорий
    await update.message.reply_text(reply)
    await update.message.reply_text("Хотите удалить какие-то из них?", reply_markup=get_markup(7))
    return 'delete_categories_which'
