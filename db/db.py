from db.db_connection import get_connection


async def get_alterations_by_date(dates, username):
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
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                             "WHERE user_id=%s ORDER BY date", [username])
        return await cursor.fetchall()


async def get_category_name_by_id(i):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT name FROM categories WHERE id=%s", [i])
        return await cursor.fetchone()


async def del_alterations_by_ids(ids):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(ids) > 1:
            await cursor.execute(f"DELETE FROM alterations WHERE id IN {tuple(ids)}")
        else:
            await cursor.execute("DELETE FROM alterations WHERE id=%s", ids)
        await connection.commit()


async def del_user(username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("DELETE FROM users WHERE tg_username=%s", [username])
        await connection.commit()


async def get_categories_by_username(username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT (name) FROM categories WHERE user_id=%s", [username])
        return await cursor.fetchall()


async def get_category_id(username, category_name):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT id FROM categories WHERE name=%s AND user_id=%s", [category_name, username])
        category_id = await cursor.fetchone()
        if category_id is None or not category_id:
            await add_category(category_name, username)
        await cursor.execute("SELECT id FROM categories WHERE name=%s AND user_id=%s", [category_name, username])
        category_id = await cursor.fetchone()
    return category_id


async def add_category(category_name, username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("INSERT INTO categories (name, user_id) VALUES (%s, %s)", [category_name, username])
        await connection.commit()


async def add_alteration(*row):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute(f"INSERT INTO alterations (user_id, category_id, summa, description, date) "
                             f"VALUES (%s, %s, %s, %s, %s)", row)
        await connection.commit()


async def get_user(username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE tg_username=%s", [username])
        return await cursor.fetchone()


async def add_user_if_not_exists(username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        user = await get_user(username)
        if user is None or not user:
            await cursor.execute(f"INSERT INTO users VALUES (%s);", [username])
            await connection.commit()
            return False
        return True


async def del_categories_by_ids(ids):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(ids) > 1:
            await cursor.execute(f"DELETE FROM categories WHERE id IN {tuple(ids)}")
        else:
            await cursor.execute("DELETE FROM categories WHERE id=%s", ids)
        await connection.commit()
