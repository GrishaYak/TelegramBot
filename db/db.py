import psycopg
from db_connection import get_connection


async def get_alts(dates, username):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if len(dates) == 1:
            await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                                 "WHERE user_id=%s AND date=%s ORDER BY date", [username, dates[0]])
        else:
            await cursor.execute("SELECT (id, summa, category_id, description, date) FROM alterations "
                                 "WHERE user_id=%s AND date BETWEEN %s and %s ORDER BY date", [username, *dates])
        return await cursor.fetchall()


async def get_all_alts(username):
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
