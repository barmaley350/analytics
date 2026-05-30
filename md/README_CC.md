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

## Создание структуры таблицы из файла

Добавить данные из файла в таблицу можно двумя способами - из локального файла который находится на локальном компьютере либо из файла который смонтирован в `docker`. В первом случае используется относительный пусть к локальному файлу `./datasets/raw_data/liquor/Liquor_Sales.csv`. Во втором случае относительный путь к файлу в рамках `docker` - `./raw_data/liquor/Liquor_Sales.csv`. Файлы в `docker` находятся в директории `/var/lib/clickhouse/user_files`

Для создания структуры таблицы из файла нужно выполнить следующую последовательность команд. Все команды выполняются на локальном компьютере.

### Создание базы данных если не существует.
```
clickhouse-client -q "CREATE DATABASE IF NOT EXISTS liquor;"
```
### Удаление таблицы если существует
```
clickhouse-client -q "DROP TABLE IF EXISTS liquor.liquor2;"
```
### Создание структуры таблицы если не существует (через `docker`) 
```
clickhouse-client -q "CREATE TABLE IF NOT EXISTS liquor.liquor2 ENGINE = MergeTree ORDER BY tuple() EMPTY AS SELECT * FROM file('./raw_data/liquor/Liquor_Sales.csv');"
```
### Добавление данных в таблицу (локальный файл)
```
clickhouse-client -q "INSERT INTO liquor.liquor2 FORMAT CSVWithNames" < ./datasets/raw_data/liquor/Liquor_Sales.csv
```
```
45.66s user 9.42s system 92% cpu 59.322 total
```
### Добавление данных в таблицу (через `docker`)
```
clickhouse-client -q "INSERT INTO liquor.liquor2 SELECT * FROM file('./raw_data/liquor/Liquor_Sales.csv', CSVWithNames)"
```
```
0.09s user 0.07s system 0% cpu 22.743 total
```