import psycopg
# Этот файл нужен для подключения к базе данных PostgreSQL
CONNECTION = None


async def connect_to_db() -> psycopg.AsyncConnection:
    """Создаёт и возвращает переменную подключения к базе данных"""
    return await psycopg.AsyncConnection.connect("dbname=FinancesBot user=postgres password=123")


async def get_connection():
    """Возвращает одну глобальную переменную подключения к базе данных, и, если она ещё не была создана,
    перед этим её создаёт."""
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = await connect_to_db()
    return CONNECTION
