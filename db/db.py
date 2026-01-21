from httpcore import request
from decimal import Decimal
from .db_connection import get_connection

# В этом файле содержатся все функции с запросами в базу данных


async def get_alterations_by_date(dates, username):
    """Возвращает изменения, сделанные данным пользователем в данную дату,
    или в промежутке между двумя данными датами"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(dates) == 1:
            await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                                 "WHERE user_id=%s AND date=%s ORDER BY date", [username, dates[0]])
        else:
            await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                                 "WHERE user_id=%s AND date BETWEEN %s and %s ORDER BY date", [username, *dates])
        return await cursor.fetchall()


async def get_all_alterations(username):
    """Возвращает все изменения, сделанные данным пользователем"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                             "WHERE user_id=%s ORDER BY date", [username])
        return await cursor.fetchall()


async def get_category_name_by_id(i):
    """Возвращает название категории с данным id"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT name FROM categories WHERE id=%s", [i])
        return await cursor.fetchone()


async def del_alterations_by_ids(ids):
    """Удаляет изменения с данными id"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(ids) > 1:
            await cursor.execute(f"DELETE FROM alterations WHERE id IN {tuple(ids)}")
        else:
            await cursor.execute("DELETE FROM alterations WHERE id=%s", ids)
        await connection.commit()


async def del_user(username):
    """Удаляет пользователя с данным именем пользователя"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("DELETE FROM users WHERE tg_username=%s", [username])
        await connection.commit()


async def get_categories_by_username(username):
    """Возвращает все категории, созданные данным пользователям"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT (name) FROM categories WHERE user_id=%s", [username])
        return await cursor.fetchall()

async def get_categories_by_username_and_sign(username, sign):
    """Возвращает все категории, созданные данным пользователям"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT (name) FROM categories WHERE user_id=%s AND is_income=%s", [username, sign])
        return await cursor.fetchall()

async def get_category_id(username, category_name, is_income=None):
    """Возвращает id категории с данным названием, созданной данным пользователем"""
    if is_income is None:
        db_request = ("SELECT id FROM categories WHERE name=%s AND user_id=%s", [category_name, username])
    else:
        db_request = ("SELECT id FROM categories WHERE name=%s AND user_id=%s AND is_income=%s",
                      [category_name, username, is_income])
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute(*db_request)
        category_id = await cursor.fetchone()
        if category_id is None or not category_id:
            await add_category(category_name, username, is_income)
        await cursor.execute(*db_request)
        category_id = await cursor.fetchone()
    return category_id


async def add_category(category_name, username, is_income):
    """Создаёт категорию с данным названием за данным пользователем"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("INSERT INTO categories (name, user_id, is_income) VALUES (%s, %s, %s)", [category_name,
                                                                                                username, is_income])
        await connection.commit()


async def add_alteration(user_id, category_id, summa, description, date):
    """Добавляет изменение. На вход нужны:

    * никнейм пользователя;

    * id категории, к которой принадлежит изменение;

    * сумма, на которую сделано изменение;

    * описание изменения, может быть как строка, так и None;

    * дата совершения изменения."""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute(f"INSERT INTO alterations (user_id, category_id, summa, description, date) "
                             f"VALUES (%s, %s, %s, %s, %s)", [user_id, category_id, summa, description, date])
        await connection.commit()


async def get_user(username):
    """Возвращает ник пользователя с данным ником пользователя.
    На первый взгляд бесполезно, но на деле эта функция нужна для проверки принадлежности пользователя к базе данных."""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE tg_username=%s", [username])
        return await cursor.fetchone()


async def add_user_if_not_exists(username):
    """Добавляет пользователя в базу данных. Если он уже там был, возвращает True, иначе - False"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        user = await get_user(username)
        if user is None or not user:
            await cursor.execute(f"INSERT INTO users VALUES (%s);", [username])
            await connection.commit()
            return False
        return True


async def del_categories_by_ids(ids):
    """Удаляет категории с данными id"""
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(ids) > 1:
            await cursor.execute(f"DELETE FROM categories WHERE id IN {tuple(ids)}")
        else:
            await cursor.execute("DELETE FROM categories WHERE id=%s", ids)
        await connection.commit()
