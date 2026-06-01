# Работа с `clickhouse-local`
## Конвертируем файл из `csv` в `parquet`
Для ускорения работы с локальным файлом его нужно конвертировать из `csv` в `parquet`

### Вариант №1
> [!NOTE]
> Слишком затратная по потреблению памяти команда. Компьютер может зависнуть.
```
./clickhouse local -q "SELECT * FROM file ('./datasets/raw_data/cars/cars_sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/cars/cars_sales.parquet' FORMAT Parquet"
```
```
30.91s user 16.45s system 480% cpu 9.849 total
```
### Вариант №1
```
./clickhouse local --max_memory_usage=2G --max_threads=4 -q "SELECT * FROM file ('/datasets/raw_data/cars/cars_sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/cars/cars_sales.parquet' FORMAT Parquet"
```

| Файл | Размер | 
|---------|-----------|
| cars_sales.csv | 2.0G | 
| cars_sales.parquet | 250M |
