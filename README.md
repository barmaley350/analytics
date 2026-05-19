<style>
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    padding: 8px;
    border: 1px solid #ddd;
    text-align: left;
}
</style>

# Краткое описание
Приводится пример анализа данных на основе датасета 
[https://www.kaggle.com/datasets/ekibee/car-sales-information](https://www.kaggle.com/datasets/ekibee/car-sales-information)

Данный датасет содержит информацию о продаже машин за определенные годы
по определенным регионам. 

Датасет содежит `1 294 757` записей и `19` параметров.
Общий объем данных `2.14 Gb`.

# Общая схема работы
![png](files/md/main.png?1)

# Используемые инструменты

1. **Этап подготовки данных**
    - Python3
2. **Хранение данных**
    - ClickHouse
3. **Визуализация данных**
    - JupyterLab
    - Apache Superset

# Как запустить
`docker compose  up --build`

# Доспуп к сервисам
| Сервис | Url | Описание | 
|---------|-----------|---------------|
| JupyterLab | [http://localhost:8888/](http://localhost:8888/) |  |
| Apache Superset | [http://localhost:8088/](http://localhost:8088/) |  |
| PostgreSQL | [http://localhost:5432/](http://localhost:5432/) |  |
| ClickHouse | [http://localhost:8123/](http://localhost:8123/) |  |
| smtp4dev | [http://localhost:5000/](http://localhost:5000/) | Также доступны `POP3` -`2525:25` и `110:110`|

# Демо данные
## Используемые `datasets`
| Url | Описание | 
|---------|-----------|
| [Chinook](https://www.kaggle.com/datasets/ranasabrii/chinook) | База данных Chinook представляет собой цифровой медиамагазин, включающий в себя таблицы с информацией об исполнителях, альбомах, медиафайлах, счетах и клиентах. |
| [Kaggle / Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) | Набор данных о розничных продажах в глобальном супермаркете за 4 года. |
| [Цены на недвижимость в Великобритании](https://clickhouse.com/docs/ru/getting-started/example-datasets/uk-price-paid) | Этот набор данных содержит сведения о ценах сделок с объектами недвижимости в Англии и Уэльсе. Данные доступны с 1995 года, а размер набора данных в несжатом виде составляет около 4 GiB (в ClickHouse он занимает всего около 278 MiB). |

## Дополнительные источники 

| Url | Описание | 
|---------|-----------|
| https://the-examples-book.com/projects/data-sets/ | Базовые наборы |
| https://clickhouse.com/docs/ru/getting-started/example-datasets | Big Data |

# Дополнительная информация

| Файл | Url | Описание | 
|---------|-----------|---------------|
| SQL BASE | [SQL BASE (.md)](./md/SQL_THEORY.md) | Базовые основы SQL |
| SQL EXAMPLES | [SQL EXAMPLES (.md)](./md/SQL.md) | `md` версия для изучения |
| SQL EXAMPLES | [SQL EXAMPLES (.ipynb)](./services/jupyter/data/examples.ipynb) | `ipynb` версия для изучения |
| SQLBOOK.md | [SQLBOOK.pdf](./files/SQLBOOK.pdf) | pdf версия для скачивания |

# Визуализация

|  |  |  | 
|---------|-----------|---------------|
| ![img_1](./files/dashboards/1.jpg) |  |  |
|  |  |
|  |  |