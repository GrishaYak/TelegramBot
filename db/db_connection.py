import psycopg
from os import getenv
from dotenv import load_dotenv
# Этот файл нужен для подключения к базе данных PostgreSQL
CONNECTION = None
load_dotenv()
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')


async def connect_to_db() -> psycopg.AsyncConnection:
    """Создаёт и возвращает переменную подключения к базе данных"""
    connect = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
    return await psycopg.AsyncConnection.connect(connect)


async def get_connection():
    """Возвращает одну глобальную переменную подключения к базе данных, и, если она ещё не была создана,
    перед этим её создаёт."""
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = await connect_to_db()
    return CONNECTION
