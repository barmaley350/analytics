"""Postgresql."""

import random
import secrets

from faker import Faker
from modules.db import connect, disconnect
from psycopg2.extras import execute_batch

conn = connect()
cursor = conn.cursor()

fake = Faker("ru_RU")

word_pool = set()
while len(word_pool) < 100:  # достаточно большой пул
    word_pool.add(fake.word())
word_pool = list(word_pool)
# Заполнение таблицы statuses

products = [(fake.catch_phrase(),) for _ in range(10)]
cursor.execute("TRUNCATE TABLE products RESTART IDENTITY CASCADE;")
execute_batch(
    cursor,
    "INSERT INTO products (product_name) VALUES (%s)",
    products,
    page_size=1000,  # Размер «страницы» — сколько строк за раз
)
conn.commit()

# Заполнение таблицы categories
categories = [(word,) for word in random.sample(word_pool, 5)]
cursor.execute("TRUNCATE TABLE categories RESTART IDENTITY CASCADE;")
execute_batch(
    cursor,
    "INSERT INTO categories (category_name) VALUES (%s)",
    categories,
    page_size=1000,  # Размер «страницы» — сколько строк за раз
)
conn.commit()

# Заполнение таблицы departments
departments = [(word,) for word in random.sample(word_pool, 5)]
cursor.execute("TRUNCATE TABLE departments RESTART IDENTITY CASCADE;")
execute_batch(
    cursor,
    "INSERT INTO departments (department_name) VALUES (%s)",
    departments,
    page_size=1000,  # Размер «страницы» — сколько строк за раз
)
conn.commit()

# Заполнение таблицы Customers
costomers = []
for _ in range(100):
    customer = []
    customer.append(fake.first_name())
    customer.append(fake.last_name())
    customer.append(fake.email())
    customer.append(fake.phone_number())
    costomers.append(tuple(customer))
execute_batch(
    cursor,
    "INSERT INTO customers (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
    costomers,
    page_size=1000,  # Размер «страницы» — сколько строк за раз
)
conn.commit()

# Заполняем таблицу
total_records = 1000000
batch_size = 1000  # Размер батча
batches_count = total_records // batch_size

# Начальная сумма и параметры
current_amount = 3000  # стартовая точка примерно в середине диапазона
volatility = 0.90  # 15% волатильность

print(f"Начинаем создание {total_records} записей...")

for batch_num in range(batches_count):
    # Генерируем данные для одного батча
    data = []
    for _ in range(batch_size):
        # customer_id = secrets.randbelow(4) + 1
        customer_ids = [1, 2, 3, 4]
        weights = [0.1, 0.2, 0.3, 0.4]  # Вероятности: 10%, 20%, 30%, 40%
        customer_id = random.choices(customer_ids, weights=weights)[0]

        # status_id = secrets.randbelow(4) + 1
        product_id = random.randint(1, 10)

        # category_id = secrets.randbelow(4) + 1
        category_ids = [1, 2, 3, 4]
        weights = [0.3, 0.4, 0.2, 0.1]  # Вероятности: 10%, 20%, 30%, 40%
        category_id = random.choices(category_ids, weights=weights)[0]

        # department_id = secrets.randbelow(4) + 1
        department_ids = [1, 2, 3, 4]
        weights = [0.4, 0.1, 0.2, 0.3]  # Вероятности: 10%, 20%, 30%, 40%
        department_id = random.choices(department_ids, weights=weights)[0]

        # total_amount = 1000 + secrets.randbelow(50000)
        # Случайное изменение: ±15% от текущей суммы
        change = secrets.SystemRandom().uniform(-volatility, volatility)
        current_amount = max(current_amount * (1 + change), 1000)  # минимум 1 000
        # Ограничение верхней границы
        total_amount = int(min(current_amount, 100000))

        order_date = fake.date_time_between(start_date="-3y", end_date="now")
        data.append((
            customer_id,
            product_id,
            category_id,
            department_id,
            total_amount,
            order_date,
        ))

    # Вставляем батч данных
    execute_batch(
        cursor,
        "INSERT INTO orders (customer_id, product_id, category_id, department_id, total_amount, order_date) VALUES (%s, %s,%s, %s, %s, %s)",
        data,
        page_size=batch_size,
    )

    # Коммитим каждые 10 батчей для баланса производительности и безопасности
    if (batch_num + 1) % 10 == 0:
        conn.commit()
        print(
            f"Обработано {batch_num + 1} батчей ({(batch_num + 1) * batch_size} записей)"
        )
    conn.commit()

cursor.close()
disconnect(conn)
