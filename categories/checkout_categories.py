from db import db
from general.markups import get_markup


async def checkout_categories(update, context):
    username = update.effective_user.username
    await update.message.reply_text('За вами числятся следующие категории: ')
    categories = await db.get_categories_by_username(username)
    ids = []
    for el in categories:
        i = await db.get_category_id(username, el[0])
        ids.append(i[0])
    reply = ""
    context.user_data["categories"] = {}
    for i in range(len(categories)):
        reply += f'{i + 1}) "{categories[i][0]}"\n'
        context.user_data["categories"][i + 1] = str(ids[i])
    await update.message.reply_text(reply)
    await update.message.reply_text("Хотите удалить какие-то из них?", reply_markup=get_markup(7))
    return 'delete_categories_which'
