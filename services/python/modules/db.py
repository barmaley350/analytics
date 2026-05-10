"""Postgresql."""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Получаем путь к директории, где находится текущий скрипт
current_dir = Path(__file__).parent.parent.parent

# Поднимаемся на один уровень вверх и добавляем .env
env_path = current_dir / "postgres/.env"

# Загружаем переменные из .env
load_dotenv(dotenv_path=env_path)

# Получаем параметры подключения
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT", "5432")  # значение по умолчанию
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")


def connect():
    """Main."""  # noqa: D401
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    print("Соединение с PostgreSQL установлено")
    return conn


def disconnect(conn):
    if conn:
        conn.close()
        print("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    conn = connect()
    disconnect(conn)
