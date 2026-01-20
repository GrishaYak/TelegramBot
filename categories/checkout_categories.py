from db import db
from general.markups import get_markup


async def checkout_categories(update, context):
    """Выводит все категории пользователя, спрашивает что он хочет делать дальше."""
    username = update.effective_user.username
    # categories = await db.get_categories_by_username(username)
    incomes = await db.get_categories_by_username_and_sign(username, True)
    consumptions = await db.get_categories_by_username_and_sign(username, False)
    if not incomes and not consumptions:
        await update.message.reply_text("У вас не записано ни одной категории.", reply_markup=get_markup(1))
        return 1
    await update.message.reply_text('За вами числятся следующие категории: ')
    ids = []
    context.user_data["categories"] = {}
    if incomes:
        reply = "Категории доходов:\n"
        for el in incomes:
            i = await db.get_category_id(username, el[0])
            # выше el[0] потому, что в categories лежал картеж вида (('categ',), ('categ2',)...)
            ids.append(
                i[0])  # Здесь i[0] по схожим причинам: cursor.fetchone() и cursor.fetchall() зачем-то оборачивают
            #            всё в лишний слой картежей
        for i in range(len(incomes)):
            reply += f'{i + 1}) "{incomes[i][0]}"\n'
            context.user_data["categories"][i + 1] = str(ids[i])  # Здесь я сохраняю id категории как значение по ключу
            #  её порядкового номера, мне это пригодится, если пользователь захочет удалить какие-то из своих категорий
        await update.message.reply_text(reply)
    if consumptions:
        reply =  "Категории расходов:\n"
        for el in consumptions:
            i = await db.get_category_id(username, el[0])
            ids.append(i[0])
        for i in range(len(consumptions)):
            reply += f'{i + 1 + len(incomes)}) "{consumptions[i][0]}"\n'
            context.user_data["categories"][i + 1 + len(incomes)] = str(ids[i])
        await update.message.reply_text(reply)
    await update.message.reply_text("Хотите удалить какие-то из них?", reply_markup=get_markup(7))
    return 'delete_categories_which'
