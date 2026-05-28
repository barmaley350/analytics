

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
| `data profilling` `визуализация`| JupyterLab | [http://localhost:8888/](http://localhost:8888/) | `Data profiling` — это процесс исследования и анализа наборов данных для понимания их структуры, содержания и качества. Цель — получить полное представление о данных перед их использованием в анализе, машинном обучении или интеграции.  |
| `визуализация` | Apache Superset | [http://localhost:8088/](http://localhost:8088/) | `Apache Superset` — это бесплатная (open‑source) платформа для исследования и визуализации данных с веб‑интерфейсом. Изначально разработана в Airbnb, затем передана в Apache Software Foundation. |
| `хранение` | ClickHouse | [http://localhost:8123/](http://localhost:8123/) | `ClickHouse` — это колоночная (столбцовая) система управления базами данных (СУБД) с открытым исходным кодом (Apache License 2.0), разработанная в Яндексе для аналитики больших объёмов данных в реальном времени. |
| `хранение` | PostgreSQL | [http://localhost:5423/](http://localhost:5423/) |  |
| `визуализация` | PostgreSQL | [http://localhost:5000/](http://localhost:5000/) | `smtp4dev` — это бесплатный open‑source‑инструмент (под лицензией Apache 2.0), эмулирующий SMTP‑сервер для тестирования и отладки отправки писем в процессе разработки.  |

## Как запустить
`docker compose  up --build`

## Визуализация

|  |  |  | 
|---------|-----------|---------------|
| ![img_1](./files/dashboards/1.jpg) | ![img_1](./files/dashboards/1.jpg) | ![img_1](./files/dashboards/1.jpg) |
|  |  |
|  |  |

```python
%load_ext autotime
%matplotlib inline
```

    The autotime extension is already loaded. To reload it, use:
      %reload_ext autotime
    time: 1.37 ms (started: 2026-05-28 08:28:51 +03:00)


### Замер времени выполения


```python
import time

start_time = time.perf_counter()
```

    time: 516 μs (started: 2026-05-28 08:28:51 +03:00)


### Подключаем основные модули


```python
import socket

import clickhouse_connect
import matplotlib.pyplot as plt

# import my_module.my_describe as my_describe
# import my_module.my_modules as mm
import numpy as np
import pandas as pd
import seaborn as sns
from my_module.my_func import highlight_values
# from IPython.display import display

```

    time: 1.08 ms (started: 2026-05-28 08:28:51 +03:00)


### Объявляем основные переменные
`local_host_name` - локальное имя хоста<br>
`docker_host_name` - docker имя хоста<br>
`sample_percent` - размер выборки в процентах<br>
`sample_count` - кол-во выборок<br>
`db` - база данных<br>
`table` - название таблицы<br>



```python
local_host_name = "home-NMH-WDX9"
docker_host_name = "service.db_clickhouse"

db = "cars"
table = "car_sales"

sample_percent = 0.01
sample_count = 3
```

    time: 698 μs (started: 2026-05-28 08:28:51 +03:00)


### Подключаемся к база данных `clickhouse`

Подключение к `ClickHouse` через официальный драйвер `clickhouse-connect`.<br>
Если запуск `.ipynb` происходит на локальной машине а не в `docker` то `host = "localhost"`.<br>
Иначе указывается адрес сурвиса в рамках docker - `"service.db_clickhouse"`.

Для корректной работы `home-NMH-WDX9` нужно заменить на имя вашей локальной машины.


```python
hostname = socket.gethostname()
host = docker_host_name
if hostname == local_host_name:
    host = "localhost"

client = clickhouse_connect.get_client(
    host=host, port=8123, username="default", password=""
)
```

    time: 28.6 ms (started: 2026-05-28 08:28:51 +03:00)


### Получаем общее кол-во записей в таблице `car_sales`

Получаем общее кол-во записей в таблице `car_sales`. 

На основании полученной информаци формируем размер выборки `sample_size`. <br>
Размер выборки формируется в зависимости от значения `sample_percent`, которое задается в процентах от общего кол-ва записей в таблице.


```python
sql = f"SELECT COUNT(*) FROM {db}.{table};"  # noqa: S608
result = client.query(sql)
rows_count = result.result_rows[0][0]
sample_size = round(rows_count * sample_percent)
info_dict = {
    "Metric": [
        f"Кол-во записей в таблице {db}.{table}",
        f"Размер выборки ({sample_percent * 100}%)",
    ],
    "Value": [f"{rows_count:_d}", f"{sample_size:_d}"],
}
info_df = pd.DataFrame(info_dict)
info_df
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Metric</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Кол-во записей в таблице cars.car_sales</td>
      <td>1_294_757</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Размер выборки (1.0%)</td>
      <td>12_948</td>
    </tr>
  </tbody>
</table>
</div>



    time: 18.1 ms (started: 2026-05-28 08:28:51 +03:00)


### Формирование отчета аналогичного `pandas` -  `df.info()`


```python
sql = f"DESCRIBE TABLE {db}.{table}"
result = client.query_df(sql).set_index("name")

cars_columns = result.index.to_list()

field_not_null_counts = {}
for column in cars_columns:
    sql = f"""SELECT
    count(*) as count_{column}
    FROM {db}.{table}
    WHERE {column} IS NOT NULL"""  # noqa: S608
    field_not_null_counts[column] = client.query(sql).result_rows[0][0]
df = pd.DataFrame.from_dict(
    field_not_null_counts, orient="index", columns=["Non-Null Count"]
)

df["Null Count"] = rows_count - df["Non-Null Count"]
df["Null Count %"] = round((df["Null Count"] * 100) / rows_count, 2)

rez = pd.concat([result, df], axis=1).reset_index().rename(columns={"index": "field"})
rez = rez[["field", "type", "Non-Null Count", "Null Count", "Null Count %"]]
rez["Null Count %"] = pd.to_numeric(rez["Null Count %"], errors="coerce")
rez["Description"] = np.where(df["Null Count %"] > 30, "Много", "")

threshold = 30
rez_styled = rez.style.map(
    lambda val: highlight_values(val, threshold=threshold), subset=["Null Count %"]
).format({"Null Count %": "{:.2f}"})

rez_styled
```





<table id="T_1a12c">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_1a12c_level0_col0" class="col_heading level0 col0" >field</th>
      <th id="T_1a12c_level0_col1" class="col_heading level0 col1" >type</th>
      <th id="T_1a12c_level0_col2" class="col_heading level0 col2" >Non-Null Count</th>
      <th id="T_1a12c_level0_col3" class="col_heading level0 col3" >Null Count</th>
      <th id="T_1a12c_level0_col4" class="col_heading level0 col4" >Null Count %</th>
      <th id="T_1a12c_level0_col5" class="col_heading level0 col5" >Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_1a12c_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_1a12c_row0_col0" class="data row0 col0" >brand</td>
      <td id="T_1a12c_row0_col1" class="data row0 col1" >Nullable(String)</td>
      <td id="T_1a12c_row0_col2" class="data row0 col2" >1294757</td>
      <td id="T_1a12c_row0_col3" class="data row0 col3" >0</td>
      <td id="T_1a12c_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_1a12c_row0_col5" class="data row0 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_1a12c_row1_col0" class="data row1 col0" >name</td>
      <td id="T_1a12c_row1_col1" class="data row1 col1" >Nullable(String)</td>
      <td id="T_1a12c_row1_col2" class="data row1 col2" >1294757</td>
      <td id="T_1a12c_row1_col3" class="data row1 col3" >0</td>
      <td id="T_1a12c_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_1a12c_row1_col5" class="data row1 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_1a12c_row2_col0" class="data row2 col0" >bodyType</td>
      <td id="T_1a12c_row2_col1" class="data row2 col1" >Nullable(String)</td>
      <td id="T_1a12c_row2_col2" class="data row2 col2" >1294757</td>
      <td id="T_1a12c_row2_col3" class="data row2 col3" >0</td>
      <td id="T_1a12c_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_1a12c_row2_col5" class="data row2 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_1a12c_row3_col0" class="data row3 col0" >color</td>
      <td id="T_1a12c_row3_col1" class="data row3 col1" >Nullable(String)</td>
      <td id="T_1a12c_row3_col2" class="data row3 col2" >1257029</td>
      <td id="T_1a12c_row3_col3" class="data row3 col3" >37728</td>
      <td id="T_1a12c_row3_col4" class="data row3 col4" >2.91</td>
      <td id="T_1a12c_row3_col5" class="data row3 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_1a12c_row4_col0" class="data row4 col0" >fuelType</td>
      <td id="T_1a12c_row4_col1" class="data row4 col1" >Nullable(String)</td>
      <td id="T_1a12c_row4_col2" class="data row4 col2" >1289815</td>
      <td id="T_1a12c_row4_col3" class="data row4 col3" >4942</td>
      <td id="T_1a12c_row4_col4" class="data row4 col4" >0.38</td>
      <td id="T_1a12c_row4_col5" class="data row4 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_1a12c_row5_col0" class="data row5 col0" >year</td>
      <td id="T_1a12c_row5_col1" class="data row5 col1" >Nullable(UInt32)</td>
      <td id="T_1a12c_row5_col2" class="data row5 col2" >724644</td>
      <td id="T_1a12c_row5_col3" class="data row5 col3" >570113</td>
      <td id="T_1a12c_row5_col4" class="data row5 col4" >44.03</td>
      <td id="T_1a12c_row5_col5" class="data row5 col5" >Много</td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_1a12c_row6_col0" class="data row6 col0" >mileage</td>
      <td id="T_1a12c_row6_col1" class="data row6 col1" >Nullable(UInt32)</td>
      <td id="T_1a12c_row6_col2" class="data row6 col2" >771799</td>
      <td id="T_1a12c_row6_col3" class="data row6 col3" >522958</td>
      <td id="T_1a12c_row6_col4" class="data row6 col4" >40.39</td>
      <td id="T_1a12c_row6_col5" class="data row6 col5" >Много</td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_1a12c_row7_col0" class="data row7 col0" >transmission</td>
      <td id="T_1a12c_row7_col1" class="data row7 col1" >Nullable(String)</td>
      <td id="T_1a12c_row7_col2" class="data row7 col2" >1289563</td>
      <td id="T_1a12c_row7_col3" class="data row7 col3" >5194</td>
      <td id="T_1a12c_row7_col4" class="data row7 col4" >0.40</td>
      <td id="T_1a12c_row7_col5" class="data row7 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_1a12c_row8_col0" class="data row8 col0" >power</td>
      <td id="T_1a12c_row8_col1" class="data row8 col1" >Nullable(UInt16)</td>
      <td id="T_1a12c_row8_col2" class="data row8 col2" >1273353</td>
      <td id="T_1a12c_row8_col3" class="data row8 col3" >21404</td>
      <td id="T_1a12c_row8_col4" class="data row8 col4" >1.65</td>
      <td id="T_1a12c_row8_col5" class="data row8 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_1a12c_row9_col0" class="data row9 col0" >price</td>
      <td id="T_1a12c_row9_col1" class="data row9 col1" >UInt32</td>
      <td id="T_1a12c_row9_col2" class="data row9 col2" >1294757</td>
      <td id="T_1a12c_row9_col3" class="data row9 col3" >0</td>
      <td id="T_1a12c_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_1a12c_row9_col5" class="data row9 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_1a12c_row10_col0" class="data row10 col0" >vehicleConfiguration</td>
      <td id="T_1a12c_row10_col1" class="data row10 col1" >Nullable(String)</td>
      <td id="T_1a12c_row10_col2" class="data row10 col2" >724647</td>
      <td id="T_1a12c_row10_col3" class="data row10 col3" >570110</td>
      <td id="T_1a12c_row10_col4" class="data row10 col4" >44.03</td>
      <td id="T_1a12c_row10_col5" class="data row10 col5" >Много</td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_1a12c_row11_col0" class="data row11 col0" >engineName</td>
      <td id="T_1a12c_row11_col1" class="data row11 col1" >Nullable(String)</td>
      <td id="T_1a12c_row11_col2" class="data row11 col2" >720976</td>
      <td id="T_1a12c_row11_col3" class="data row11 col3" >573781</td>
      <td id="T_1a12c_row11_col4" class="data row11 col4" >44.32</td>
      <td id="T_1a12c_row11_col5" class="data row11 col5" >Много</td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_1a12c_row12_col0" class="data row12 col0" >engineDisplacement</td>
      <td id="T_1a12c_row12_col1" class="data row12 col1" >Nullable(Float64)</td>
      <td id="T_1a12c_row12_col2" class="data row12 col2" >717625</td>
      <td id="T_1a12c_row12_col3" class="data row12 col3" >577132</td>
      <td id="T_1a12c_row12_col4" class="data row12 col4" >44.57</td>
      <td id="T_1a12c_row12_col5" class="data row12 col5" >Много</td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_1a12c_row13_col0" class="data row13 col0" >date</td>
      <td id="T_1a12c_row13_col1" class="data row13 col1" >Date</td>
      <td id="T_1a12c_row13_col2" class="data row13 col2" >1294757</td>
      <td id="T_1a12c_row13_col3" class="data row13 col3" >0</td>
      <td id="T_1a12c_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_1a12c_row13_col5" class="data row13 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_1a12c_row14_col0" class="data row14 col0" >location</td>
      <td id="T_1a12c_row14_col1" class="data row14 col1" >Nullable(String)</td>
      <td id="T_1a12c_row14_col2" class="data row14 col2" >1294757</td>
      <td id="T_1a12c_row14_col3" class="data row14 col3" >0</td>
      <td id="T_1a12c_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_1a12c_row14_col5" class="data row14 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_1a12c_row15_col0" class="data row15 col0" >link</td>
      <td id="T_1a12c_row15_col1" class="data row15 col1" >Nullable(String)</td>
      <td id="T_1a12c_row15_col2" class="data row15 col2" >1294757</td>
      <td id="T_1a12c_row15_col3" class="data row15 col3" >0</td>
      <td id="T_1a12c_row15_col4" class="data row15 col4" >0.00</td>
      <td id="T_1a12c_row15_col5" class="data row15 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_1a12c_row16_col0" class="data row16 col0" >description</td>
      <td id="T_1a12c_row16_col1" class="data row16 col1" >Nullable(String)</td>
      <td id="T_1a12c_row16_col2" class="data row16 col2" >1254405</td>
      <td id="T_1a12c_row16_col3" class="data row16 col3" >40352</td>
      <td id="T_1a12c_row16_col4" class="data row16 col4" >3.12</td>
      <td id="T_1a12c_row16_col5" class="data row16 col5" ></td>
    </tr>
    <tr>
      <th id="T_1a12c_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_1a12c_row17_col0" class="data row17 col0" >parse_date</td>
      <td id="T_1a12c_row17_col1" class="data row17 col1" >DateTime</td>
      <td id="T_1a12c_row17_col2" class="data row17 col2" >1294757</td>
      <td id="T_1a12c_row17_col3" class="data row17 col3" >0</td>
      <td id="T_1a12c_row17_col4" class="data row17 col4" >0.00</td>
      <td id="T_1a12c_row17_col5" class="data row17 col5" ></td>
    </tr>
  </tbody>
</table>




    time: 429 ms (started: 2026-05-28 08:28:51 +03:00)



```python
n = rez["Null Count"].sum()
null_dict = {
    "Null Values Count": n,
    "All Values Count": rows_count * len(rez),
    "Percent (%)": (n * 100) / (rows_count * len(rez)),
}
null_dict_df = pd.DataFrame(null_dict, index=[0])
null_dict_df
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Null Values Count</th>
      <th>All Values Count</th>
      <th>Percent (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2923714</td>
      <td>23305626</td>
      <td>12.5451</td>
    </tr>
  </tbody>
</table>
</div>



    time: 10 ms (started: 2026-05-28 08:28:51 +03:00)



```python
filtered_data = rez[rez["Null Count"] > 0]
plt.bar(filtered_data["field"], filtered_data["Null Count"])

plt.title("Столбчатая диаграмма для полей с NULL-значениями")
plt.xlabel("Поля")
plt.ylabel("Количество NULL")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

```


    
![png](files/jupyter/images/output_14_0.png)
    


    time: 275 ms (started: 2026-05-28 08:28:51 +03:00)


### Формирование отчета аналогичного `pandas` -  `df.describe()`


```python
fields = ["price", "year", "mileage", "power"]
agg_funcs = {
    "count": "count",
    "mean": "avg",
    "std": "stddevPop",
    "min": "min",
    "25%": "quantile(0.25)",
    "50%": "quantile(0.50)",
    "75%": "quantile(0.75)",
    "max": "max",
}
totals = {}
for field in fields:
    totals[f"total_{field}"] = {}
    for key, func in agg_funcs.items():
        sql = f"""SELECT {func}({field}) FROM {db}.{table};"""  # noqa: S608
        result = client.query(sql)
        totals[f"total_{field}"].setdefault(key, 0)
        totals[f"total_{field}"][key] = result.result_rows[0][0]
totals_df = pd.DataFrame(totals)
with pd.option_context(
    "display.float_format",
    "{:.2f}".format,
    "display.expand_frame_repr",
    False,
):
    display(totals_df)

```


<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>total_price</th>
      <th>total_year</th>
      <th>total_mileage</th>
      <th>total_power</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1294757.00</td>
      <td>724644.00</td>
      <td>771799.00</td>
      <td>1273353.00</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1444357.82</td>
      <td>2009.68</td>
      <td>154893.40</td>
      <td>141.56</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1970256.65</td>
      <td>9.37</td>
      <td>100738.27</td>
      <td>65.64</td>
    </tr>
    <tr>
      <th>min</th>
      <td>270.00</td>
      <td>1936.00</td>
      <td>1000.00</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>425000.00</td>
      <td>2004.00</td>
      <td>84000.00</td>
      <td>98.00</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>869999.50</td>
      <td>2011.00</td>
      <td>145000.00</td>
      <td>128.00</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1739250.00</td>
      <td>2017.00</td>
      <td>211250.00</td>
      <td>163.00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>150000000.00</td>
      <td>2023.00</td>
      <td>1000000.00</td>
      <td>1000.00</td>
    </tr>
  </tbody>
</table>
</div>


    time: 475 ms (started: 2026-05-28 08:28:52 +03:00)


### Формирование нескольких выборок



```python
cars_columns2 = cars_columns.copy()
cars_columns2.remove("link")
cars_columns2.remove("description")

dfs = []
sample_count = 3
sql = f"""
WITH ranked AS (
    SELECT
        {",".join(cars_columns2)},
        NTILE({sample_count}) OVER (ORDER BY rand()) AS tile
    FROM cars.car_sales
),
ranked_with_row_num AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY tile ORDER BY rand()) AS row_num
    FROM ranked
)
SELECT *
FROM ranked_with_row_num
WHERE row_num <= {sample_size}
"""  # noqa: S608
df = client.query_df(sql)
df_renamed = df.rename(
    columns={"engineDisplacement": "ED", "vehicleConfiguration": "VC"}
)

for group_id in range(1, sample_count + 1):
    dfs.append(df_renamed[df_renamed["tile"] == group_id])  # noqa: PERF401

```

    time: 3.24 s (started: 2026-05-28 08:28:52 +03:00)



```python
dfs[0].sample(5)
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>brand</th>
      <th>name</th>
      <th>bodyType</th>
      <th>color</th>
      <th>fuelType</th>
      <th>year</th>
      <th>mileage</th>
      <th>transmission</th>
      <th>power</th>
      <th>price</th>
      <th>VC</th>
      <th>engineName</th>
      <th>ED</th>
      <th>date</th>
      <th>location</th>
      <th>parse_date</th>
      <th>tile</th>
      <th>row_num</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>33853</th>
      <td>Land Rover</td>
      <td>Range Rover</td>
      <td>Джип 5 дв.</td>
      <td>Серый</td>
      <td>Дизель</td>
      <td>2012</td>
      <td>136000</td>
      <td>АКПП</td>
      <td>339</td>
      <td>4200000</td>
      <td>4.4 SD AT Autobiography</td>
      <td>448DT</td>
      <td>4.4</td>
      <td>2023-05-08</td>
      <td>Владивосток</td>
      <td>2023-05-08 17:00:00</td>
      <td>1</td>
      <td>7958</td>
    </tr>
    <tr>
      <th>28046</th>
      <td>Nissan</td>
      <td>Serena</td>
      <td>Минивэн</td>
      <td>Серый</td>
      <td>Бензин</td>
      <td>2012</td>
      <td>&lt;NA&gt;</td>
      <td>Вариатор</td>
      <td>147</td>
      <td>1249000</td>
      <td>2.0 20S</td>
      <td>MR20DD</td>
      <td>2.0</td>
      <td>2023-06-20</td>
      <td>Новосибирск</td>
      <td>2023-06-20 18:00:00</td>
      <td>1</td>
      <td>2151</td>
    </tr>
    <tr>
      <th>34773</th>
      <td>Hyundai</td>
      <td>Santa Fe</td>
      <td>Джип 5 дв.</td>
      <td>Черный</td>
      <td>Дизель</td>
      <td>&lt;NA&gt;</td>
      <td>114000</td>
      <td>Автомат</td>
      <td>185</td>
      <td>2650000</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>NaN</td>
      <td>2023-05-30</td>
      <td>Набережные Челны</td>
      <td>2023-06-02 16:00:00</td>
      <td>1</td>
      <td>8878</td>
    </tr>
    <tr>
      <th>34272</th>
      <td>Volkswagen</td>
      <td>Polo</td>
      <td>Седан</td>
      <td>Серый</td>
      <td>Бензин</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>Механика</td>
      <td>125</td>
      <td>1240000</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>NaN</td>
      <td>2023-06-17</td>
      <td>Москва</td>
      <td>2023-06-17 14:00:00</td>
      <td>1</td>
      <td>8377</td>
    </tr>
    <tr>
      <th>29695</th>
      <td>Toyota</td>
      <td>Corolla Fielder</td>
      <td>Универсал</td>
      <td>Серый</td>
      <td>Бензин</td>
      <td>2008</td>
      <td>&lt;NA&gt;</td>
      <td>Вариатор</td>
      <td>110</td>
      <td>789000</td>
      <td>1.5 X</td>
      <td>1NZ-FE</td>
      <td>1.5</td>
      <td>2023-06-09</td>
      <td>Красноярск</td>
      <td>2023-06-09 22:00:00</td>
      <td>1</td>
      <td>3800</td>
    </tr>
  </tbody>
</table>
</div>



    time: 34.2 ms (started: 2026-05-28 08:28:55 +03:00)


### Получение описательной статистики по выборкам


```python
fields = ["price", "power", "year"]
descs = []
descs.append(totals_df)
for i in range(sample_count):
    desc = dfs[i][fields].describe()
    desc.columns = [f"df{i + 1}_{col}" for col in desc.columns]
    descs.append(desc)

combined_desc = pd.concat(descs, axis=1)

with pd.option_context(
    "display.float_format",
    "{:.2f}".format,
    "display.expand_frame_repr",
    False,
):
    display(combined_desc)

```


<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>total_price</th>
      <th>total_year</th>
      <th>total_mileage</th>
      <th>total_power</th>
      <th>df1_price</th>
      <th>df1_power</th>
      <th>df1_year</th>
      <th>df2_price</th>
      <th>df2_power</th>
      <th>df2_year</th>
      <th>df3_price</th>
      <th>df3_power</th>
      <th>df3_year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1294757.00</td>
      <td>724644.00</td>
      <td>771799.00</td>
      <td>1273353.00</td>
      <td>12948.00</td>
      <td>12737.00</td>
      <td>7205.00</td>
      <td>12948.00</td>
      <td>12738.00</td>
      <td>7265.00</td>
      <td>12948.00</td>
      <td>12720.00</td>
      <td>7101.00</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1444357.82</td>
      <td>2009.68</td>
      <td>154893.40</td>
      <td>141.56</td>
      <td>1445600.69</td>
      <td>142.25</td>
      <td>2009.66</td>
      <td>1431677.25</td>
      <td>140.73</td>
      <td>2009.59</td>
      <td>1455682.63</td>
      <td>141.80</td>
      <td>2009.88</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1970256.65</td>
      <td>9.37</td>
      <td>100738.27</td>
      <td>65.64</td>
      <td>1986878.91</td>
      <td>68.07</td>
      <td>9.43</td>
      <td>2086363.50</td>
      <td>64.12</td>
      <td>9.41</td>
      <td>2061295.69</td>
      <td>66.43</td>
      <td>9.20</td>
    </tr>
    <tr>
      <th>min</th>
      <td>270.00</td>
      <td>1936.00</td>
      <td>1000.00</td>
      <td>1.00</td>
      <td>20000.00</td>
      <td>26.00</td>
      <td>1936.00</td>
      <td>15000.00</td>
      <td>30.00</td>
      <td>1943.00</td>
      <td>20000.00</td>
      <td>16.00</td>
      <td>1953.00</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>425000.00</td>
      <td>2004.00</td>
      <td>84000.00</td>
      <td>98.00</td>
      <td>420000.00</td>
      <td>98.00</td>
      <td>2003.00</td>
      <td>420000.00</td>
      <td>98.00</td>
      <td>2003.00</td>
      <td>440000.00</td>
      <td>98.00</td>
      <td>2004.00</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>869999.50</td>
      <td>2011.00</td>
      <td>145000.00</td>
      <td>128.00</td>
      <td>865000.00</td>
      <td>128.00</td>
      <td>2011.00</td>
      <td>860000.00</td>
      <td>126.00</td>
      <td>2011.00</td>
      <td>869000.00</td>
      <td>128.00</td>
      <td>2011.00</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1739250.00</td>
      <td>2017.00</td>
      <td>211250.00</td>
      <td>163.00</td>
      <td>1763437.50</td>
      <td>163.00</td>
      <td>2017.00</td>
      <td>1755000.00</td>
      <td>160.00</td>
      <td>2017.00</td>
      <td>1750000.00</td>
      <td>163.00</td>
      <td>2017.00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>150000000.00</td>
      <td>2023.00</td>
      <td>1000000.00</td>
      <td>1000.00</td>
      <td>52219080.00</td>
      <td>780.00</td>
      <td>2023.00</td>
      <td>99999999.00</td>
      <td>693.00</td>
      <td>2023.00</td>
      <td>59999999.00</td>
      <td>693.00</td>
      <td>2023.00</td>
    </tr>
  </tbody>
</table>
</div>


    time: 70.5 ms (started: 2026-05-28 08:28:55 +03:00)


### Сравнение описательной статистики по выборкам с общими данными на предмет наличия/отсутствия существенных расхождений


```python
new_df = totals_df.copy()
rows = new_df.index.tolist()
rows.remove("min")
rows.remove("max")

fields = ["price", "power", "year"]
for field in fields:
    new_df.loc[rows, f"avg_{field}"] = (
        combined_desc.loc[rows].filter(regex=rf"df\d+_{field}").sum(axis=1)
        / sample_count
    )
    new_df[f"{field}_diff"] = new_df[f"total_{field}"] - new_df[f"avg_{field}"]
    new_df[f"{field}_diff_P"] = 100 - round(
        (new_df[f"avg_{field}"] * 100) / new_df[f"total_{field}"], 2
    )

result = new_df.filter(regex="^total_|_diff_P$")

with pd.option_context(
    "display.float_format",
    "{:.2f}".format,
    "display.expand_frame_repr",
    False,
):
    display(result)

```


<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>total_price</th>
      <th>total_year</th>
      <th>total_mileage</th>
      <th>total_power</th>
      <th>price_diff_P</th>
      <th>power_diff_P</th>
      <th>year_diff_P</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1294757.00</td>
      <td>724644.00</td>
      <td>771799.00</td>
      <td>1273353.00</td>
      <td>99.00</td>
      <td>99.00</td>
      <td>99.01</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1444357.82</td>
      <td>2009.68</td>
      <td>154893.40</td>
      <td>141.56</td>
      <td>0.00</td>
      <td>-0.03</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1970256.65</td>
      <td>9.37</td>
      <td>100738.27</td>
      <td>65.64</td>
      <td>-3.79</td>
      <td>-0.86</td>
      <td>0.23</td>
    </tr>
    <tr>
      <th>min</th>
      <td>270.00</td>
      <td>1936.00</td>
      <td>1000.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>425000.00</td>
      <td>2004.00</td>
      <td>84000.00</td>
      <td>98.00</td>
      <td>-0.39</td>
      <td>0.00</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>869999.50</td>
      <td>2011.00</td>
      <td>145000.00</td>
      <td>128.00</td>
      <td>0.61</td>
      <td>0.52</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1739250.00</td>
      <td>2017.00</td>
      <td>211250.00</td>
      <td>163.00</td>
      <td>-0.97</td>
      <td>0.61</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>150000000.00</td>
      <td>2023.00</td>
      <td>1000000.00</td>
      <td>1000.00</td>
      <td>NaN</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
    </tr>
  </tbody>
</table>
</div>


    time: 43.5 ms (started: 2026-05-28 08:28:55 +03:00)



```python
row_null_count = dfs[0][["price", "year", "mileage"]].isnull().sum(axis=1)

# Параметры группировки
group_size = 1000  # размер группы строк
n_groups = len(row_null_count) // group_size

# Агрегируем: общее количество NULL для каждой группы
aggregated_counts = []
group_labels = []

for i in range(n_groups):
    start_row = i * group_size
    end_row = start_row + group_size
    group_data = row_null_count.iloc[start_row:end_row]
    aggregated_counts.append(group_data.sum())  # Суммируем все NULL в группе
    group_labels.append(f"{start_row}–{end_row - 1}")

# Строим график
fig, ax = plt.subplots(figsize=(14, 6))
bars = ax.bar(
    group_labels, aggregated_counts, color="skyblue", edgecolor="navy", alpha=0.8
)

# Добавляем значения на столбцы
ax.bar_label(
    bars,
    labels=[f"{int(val):,}" for val in aggregated_counts],
    label_type="edge",
    fontsize=10,
    color="darkblue",
    padding=3,
)

ax.set_title(f"Общее количество NULL по группам строк (группы по {group_size} строк)")
ax.set_xlabel("Диапазоны строк")
ax.set_ylabel("Общее число NULL в группе")
plt.xticks(rotation=45)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

```


    
![png](files/jupyter/images/output_24_0.png)
    


    time: 305 ms (started: 2026-05-28 08:28:56 +03:00)



```python
plt.figure(figsize=(16, 6))
for idx, df_number in enumerate(dfs, 1):
    sns.lineplot(
        x="date",
        y="price",
        data=df_number,
        linewidth=2.5,
        errorbar="sd",
        label=f"Выборка #{idx}",
    )
plt.xlabel("Дата")
plt.ylabel("Цена")
plt.show()
```


    
![png](files/jupyter/images/output_25_0.png)
    


    time: 462 ms (started: 2026-05-28 08:28:56 +03:00)



```python
for idx, df_number in enumerate(dfs):
    fig, axes = plt.subplots(1, 4, figsize=(15, 3), constrained_layout=True)
    fig.suptitle(f"Графики для выборки #{idx + 1}", fontsize=16, fontweight="bold")

    # График 1: power vs price
    sns.regplot(data=dfs[idx], x="power", y="price", ax=axes[0])
    axes[0].set_xlabel("Мощность (л.с.)")
    axes[0].set_ylabel("Цена")
    axes[0].set_title("Зависимость цены от мощности")

    # График 2: mileage vs price
    sns.regplot(data=dfs[idx], x="mileage", y="price", ax=axes[1])
    axes[1].set_xlabel("Пробег (км)")
    axes[1].set_ylabel("Цена")
    axes[1].set_title("Зависимость цены от пробега")

    # График 3: year vs price
    sns.regplot(data=dfs[idx], x="year", y="price", ax=axes[2])
    axes[2].set_xlabel("Год выпуска")
    axes[2].set_ylabel("Цена")
    axes[2].set_title("Зависимость цены от года выпуска")

    # График 4: year vs power
    sns.regplot(data=dfs[idx], x="year", y="power", ax=axes[3])
    axes[3].set_xlabel("Год выпуска")
    axes[3].set_ylabel("Мощность (л.с.)")
    axes[3].set_title("Зависимость мощности от года выпуска")

plt.show()

```


    
![png](files/jupyter/images/output_26_0.png)
    



    
![png](files/jupyter/images/output_26_1.png)
    



    
![png](files/jupyter/images/output_26_2.png)
    


    time: 4.92 s (started: 2026-05-28 08:28:56 +03:00)



```python
end_time = time.perf_counter()
total_time = end_time - start_time
print(f"Общее время выполнения: {total_time:.4f} секунд")
```

    Общее время выполнения: 10.5171 секунд
    time: 781 μs (started: 2026-05-28 08:29:01 +03:00)

