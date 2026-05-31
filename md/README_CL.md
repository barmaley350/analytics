# Работа с `clickhouse-local`
## Конвертируем файл из `csv` в `parquet`
Для ускорения работы с локальным файлом его нужно конвертировать из `csv` в `parquet`

```
./clickhouse local -q "SELECT * FROM file ('./datasets/raw_data/cars/cars_sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/cars/car_sales.parquet' FORMAT Parquet"
```
```
30.91s user 16.45s system 480% cpu 9.849 total
```
| Файл | Размер | 
|---------|-----------|
| cars_sales.csv | 2.0G | 
| cars_sales.parquet | 250M |

Разница примерно в 4 раза.

## Предварительный анализ
### Структура файла
```
./clickhouse local -q "DESCRIBE TABLE file ('./datasets/raw_data/cars/cars_sales.parquet') FORMAT Markdown"
```

| name | type | default_type | default_expression | comment | codec_expression | ttl_expression |
|:-|:-|:-|:-|:-|:-|:-|
| brand | Nullable(String) |  |  |  |  |  |
| name | Nullable(String) |  |  |  |  |  |
| bodyType | Nullable(String) |  |  |  |  |  |
| color | Nullable(String) |  |  |  |  |  |
| fuelType | Nullable(String) |  |  |  |  |  |
| year | Nullable(Float64) |  |  |  |  |  |
| mileage | Nullable(Float64) |  |  |  |  |  |
| transmission | Nullable(String) |  |  |  |  |  |
| power | Nullable(Float64) |  |  |  |  |  |
| price | Nullable(Int64) |  |  |  |  |  |
| vehicleConfiguration | Nullable(String) |  |  |  |  |  |
| engineName | Nullable(String) |  |  |  |  |  |
| engineDisplacement | Nullable(String) |  |  |  |  |  |
| date | Nullable(DateTime64(3, \'UTC\')) |  |  |  |  |  |
| location | Nullable(String) |  |  |  |  |  |
| link | Nullable(String) |  |  |  |  |  |
| description | Nullable(String) |  |  |  |  |  |
| parse_date | Nullable(DateTime64(3, \'UTC\')) |  |  |  |  |  |
