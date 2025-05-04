import psycopg


CONNECTION = None


async def connect_to_db() -> psycopg.AsyncConnection:
    return await psycopg.AsyncConnection.connect("dbname=FinancesBot user=postgres password=123")


async def get_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = await connect_to_db()
    return CONNECTION
