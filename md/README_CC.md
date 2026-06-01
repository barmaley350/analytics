# Работа с `clickhouse-client`
## Описание
В данном проекте для работы с данными используется `clickhouse server` который работает в рамках `docker`. 

Для более быстрого предварительного анализа можно также использвать `clickhouse-local` для 
непосредственной работы с файлаим. 

Для более быстрой работы рекомендуется предварительно конвертировать `csv` и другие текстовые форматы файлов в `parquet` формат. 

## Настройка `docker`
Для того чтобы была возможность работать с файлами данных в `docker` при использвании 
`clickhouse-client` нужно смонтировать локальную папку где лежать данные в `docker`.

По умолчанию `clickhouse` ищет файлы с данными в папке `/var/lib/clickhouse/user_files`.

Для того чтобы работать с локальной папкой с данными в `docker` нужно добавить в `docker-compose.yaml` следующие настройки 

```
volumes:
    - ./datasets:/var/lib/clickhouse/user_files
```
Где `./datasets` относительный или абсолютный путь к папке с данными.

## Создание структуры таблицы из файла (CLI)

Добавить данные из файла в таблицу можно двумя способами - из локального файла который находится на локальном компьютере либо из файла который смонтирован в `docker`. В первом случае используется относительный пусть к локальному файлу `./datasets/raw_data/cars/cars_sales.csv`. Во втором случае относительный путь к файлу в рамках `docker` - `./raw_data/cars/cars_sales.csv`. Файлы в `docker` находятся в директории `/var/lib/clickhouse/user_files`

Для создания структуры таблицы из файла нужно выполнить следующую последовательность команд. Все команды выполняются на локальном компьютере.

### Создание базы данных если не существует.
```
clickhouse-client -q "CREATE DATABASE IF NOT EXISTS cars;"
```
### Удаление таблицы если существует
```
clickhouse-client -q "DROP TABLE IF EXISTS cars.cars_sales;"
```
### Создание структуры таблицы если не существует (через `docker`) 
```
clickhouse-client -q "CREATE TABLE IF NOT EXISTS cars.cars_sales ENGINE = MergeTree ORDER BY tuple() EMPTY AS SELECT * FROM file('./raw_data/cars/cars_sales.csv');"
```
или `parquet` файл
```
clickhouse-client -q "CREATE TABLE IF NOT EXISTS cars.cars_sales ENGINE = MergeTree ORDER BY tuple() EMPTY AS SELECT * FROM file('./raw_data/cars/cars_sales.parquet');"
```
### Добавление данных в таблицу (локальный файл)
```
clickhouse-client -q "INSERT INTO cars.cars_sales FORMAT CSVWithNames" < ./datasets/raw_data/cars/cars_sales.csv
```
```
5.55s user 4.89s system 46% cpu 22.242 total
```
или `parquet` файл
```
clickhouse-client -q "INSERT INTO cars.cars_sales FORMAT Parquet" < ./datasets/raw_data/cars/cars_sales.parquet
```
```
7.01s user 4.55s system 40% cpu 28.321 total
```
### Добавление данных в таблицу (через `docker`)
```
clickhouse-client -q "INSERT INTO cars.cars_sales SELECT * FROM file('./raw_data/cars/cars_sales.csv', CSVWithNames)"
```
```
0.05s user 0.03s system 1% cpu 7.224 total
```
или `parquet` файл
```
clickhouse-client -q "INSERT INTO cars.cars_sales SELECT * FROM file('./raw_data/cars/cars_sales.parquet', Parquet)"
```
> [!WARNING]
> Code: 241. DB::Exception: Received from localhost:9000. DB::Exception: (total) memory limit exceeded: would use 3.24 GiB (attempt to allocate chunk of 33.22 MiB), current RSS: 2.11 GiB, maximum: 3.21 GiB. OvercommitTracker decision: Query was selected to stop by OvercommitTracker: read stage: ColumnData: column: description: (in file/uri /var/lib/clickhouse/user_files/raw_data/cars/cars_sales.parquet): While executing ParquetV3BlockInputFormat: While executing File. (MEMORY_LIMIT_EXCEEDED)

> [!WARNING]
> Так и не удалось загрузить `parque` файл. Возможно используется какая-то другая логика. С загрузкой `csv` проблем нет.

## Создание структуры таблицы из файла (.sql)
Проще создать предварительно `sql` файл и рабоать с ним.
```sql
DROP DATABASE IF EXISTS cars;

CREATE DATABASE IF NOT EXISTS cars;

DROP TABLE IF EXISTS cars.cars_sales;

CREATE TABLE IF NOT EXISTS cars.cars_sales (
    brand Nullable(String),
    name Nullable(String),
    bodyType Nullable(String),
    color LowCardinality(Nullable(String)),
    fuelType LowCardinality(Nullable(String)),
    year Nullable(UInt16),
    mileage Nullable(UInt32),
    transmission LowCardinality(Nullable(String)),
    power Nullable(UInt16),
    price UInt32,
    vehicleConfiguration LowCardinality(Nullable(String)),
    has_awd Nullable(Bool),
    engineName LowCardinality(Nullable(String)),
    engineVolume Nullable(Float32),
    date Date,
    location LowCardinality(Nullable(String)),
    parse_date DateTime
)
ENGINE = MergeTree()
ORDER BY (brand, date, parse_date)
SETTINGS allow_nullable_key = 1;

INSERT INTO cars.cars_sales
SELECT
    nullIf(brand, '') as brand,
    nullIf(name, '') as name,
    nullIf(bodyType, '') as bodyType,
    nullIf(color, '') as color,
    nullIf(fuelType, '') as fuelType,
    toUInt16OrNull(toString(toFloat32OrNull(year))) as year,
    toUInt32OrNull(toString(toFloat32OrNull(mileage))) as mileage,
    nullIf(replaceAll(transmission, 'Автомат', 'АКПП'),'') AS transmission,
    toUInt16OrNull(toString(toFloat32OrNull(power))) as power,
    toUInt32OrNull(price) as price,
    nullIf(vehicleConfiguration, '') as vehicleConfiguration,

    if(
        vehicleConfiguration IS NULL,
        NULL,
        vehicleConfiguration LIKE '%AWD%'
    ) AS has_awd,


    nullIf(engineName, '') as engineName,
    toFloat32OrNull(extract(engineDisplacement, '\\d+\\.?\\d*')) as engineVolume,
    parseDateTimeBestEffort(date) as date,
    nullIf(location, '') as location,
    parseDateTimeBestEffort(parse_date) as parse_date
FROM file(
    '/var/lib/clickhouse/user_files/raw_data/cars/cars_sales.csv',
    'CSVWithNames',
    'brand String,
     name String,
     bodyType String,
     color String,
     fuelType String,
     year String,
     mileage String,
     transmission String,
     power String,
     price String,
     vehicleConfiguration String,
     engineName String,
     engineDisplacement String,
     date String,
     location String,
     link String,
     description String,
     parse_date String'
)
SETTINGS format_csv_delimiter = ',';

```
Далее 
```
clickhouse-client < ./services/clickhouse/sql/cars2.sql 
```
## Размер таблиц
```sql
clickhouse-client -q "SELECT
    concat(database, '.', table) AS table,
    formatReadableSize(sum(bytes_on_disk)) AS size,
    sum(bytes_on_disk) AS bytes_size,
    sum(rows) AS rows,
    any(engine) AS engine
FROM system.parts
WHERE active AND table LIKE 'cars%'
GROUP BY database, table
ORDER BY bytes_size DESC
FORMAT Markdown;"
```
| table | size | bytes_size | rows | engine |
|:-|:-|-:|-:|:-|
| cars.cars_sales_parquet | 579.83 MiB | 607991068 | 1294757 | MergeTree |
| cars.cars_sales_csv | 579.63 MiB | 607788085 | 1294757 | MergeTree |
| cars.cars_sales | 31.61 MiB | 33149835 | 1294757 | MergeTree |
