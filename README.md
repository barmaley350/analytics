## Краткое описание
Приводится пример анализа данных на основе датасета 
[https://www.kaggle.com/datasets/ekibee/car-sales-information](https://www.kaggle.com/datasets/ekibee/car-sales-information)

Данный датасет содержит информацию о продаже машин за определенные годы
по определенным регионам. 

Датасет содежит `1 294 757` записей и `19` параметров.
Общий объем данных `2.14 Gb`.

## Общая схема работы
![png](files/md/main.png?1)

## Используемые инструменты

| Этап | Сервис | Url | Описание | 
|---------|---------|-----------|---------------|
| `подготовка` | python3 |  | |
| `data profilling`| JupyterLab | [http://localhost:8888/](http://localhost:8888/) | Data profiling — это процесс исследования и анализа наборов данных для понимания их структуры, содержания и качества. Цель — получить полное представление о данных перед их использованием в анализе, машинном обучении или интеграции.  |
| `визуализация` | Apache Superset | [http://localhost:8088/](http://localhost:8088/) | Apache Superset — это бесплатная (open‑source) платформа для исследования и визуализации данных с веб‑интерфейсом. Изначально разработана в Airbnb, затем передана в Apache Software Foundation. |
| `хранение` | ClickHouse | [http://localhost:8123/](http://localhost:8123/) | ClickHouse — это колоночная (столбцовая) система управления базами данных (СУБД) с открытым исходным кодом (Apache License 2.0), разработанная в Яндексе для аналитики больших объёмов данных в реальном времени. |


## Как запустить
`docker compose  up --build`

## Доспуп к сервисам
| Сервис | Url | Описание | 
|---------|-----------|---------------|
| JupyterLab | [http://localhost:8888/](http://localhost:8888/) |  |
| Apache Superset | [http://localhost:8088/](http://localhost:8088/) |  |
| PostgreSQL | [http://localhost:5432/](http://localhost:5432/) |  |
| ClickHouse | [http://localhost:8123/](http://localhost:8123/) |  |
| smtp4dev | [http://localhost:5000/](http://localhost:5000/) | |

## Дополнительные источники демо данных

| Url | Описание | 
|---------|-----------|
| https://the-examples-book.com/projects/data-sets/ | Базовые наборы |
| https://clickhouse.com/docs/ru/getting-started/example-datasets | Big Data |
| https://www.kaggle.com/datasets/ | Много разных и интересных datasets |

## Дополнительная информация

| Файл | Url | Описание | 
|---------|-----------|---------------|
| SQL BASE | [SQL BASE (.md)](./md/SQL_THEORY.md) | Базовые основы SQL |
| SQL EXAMPLES | [SQL EXAMPLES (.md)](./md/SQL.md) | `md` версия для изучения |
| SQL EXAMPLES | [SQL EXAMPLES (.ipynb)](./services/jupyter/data/examples.ipynb) | `ipynb` версия для изучения |
| SQLBOOK.md | [SQLBOOK.pdf](./files/SQLBOOK.pdf) | pdf версия для скачивания |

## Визуализация

|  |  |  | 
|---------|-----------|---------------|
| ![img_1](./files/dashboards/1.jpg) |  |  |
|  |  |
|  |  |