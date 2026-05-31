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
