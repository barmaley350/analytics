# Работа с `clickhouse-local`
## Конвертируем файлы из `csv` в `parquet`

> [!NOTE]
> Используйте `--max_memory_usage=2G` и `--max_threads=1` для слабых компьютеров

## Файл `cars_sales.csv`
### Конвертируем `csv` в `parquet`
```
./clickhouse local \
    --max_memory_usage=2G \
    --max_threads=1 \
    --output_format_parquet_compression=zstd \
    -q "SELECT * FROM file('./datasets/raw_data/cars/cars_sales.csv', 'CSVWithNames') \
    INTO OUTFILE './datasets/raw_data/cars/cars_sales_zstd.parquet' FORMAT Parquet"
```
### Вывод статистики `/usr/bin/time -v`
```
	User time (seconds): 11.84
	System time (seconds): 4.29
	Percent of CPU this job got: 138%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:11.63
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 3987284
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 8980
	Minor (reclaiming a frame) page faults: 1209593
	Voluntary context switches: 24432
	Involuntary context switches: 323
	Swaps: 0
	File system inputs: 3901832
	File system outputs: 510896
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```
### Размеры `parquet` файлов в зависимости от типа компрессии
```
ls -alhS datasets/raw_data/cars | grep -v '^d' | xclip -sel clip
```
```
-rw-rw-r-- 1 home home 2.0G May 20 08:55 cars_sales.csv
-rw-rw-r-- 1 home home 1.9G Jun  2 01:15 cars_sales_none.parquet
-rw-rw-r-- 1 home home 639M Jun  2 01:15 cars_sales_snappy.parquet
-rw-rw-r-- 1 home home 532M Jun  2 01:15 cars_sales_lz4.parquet
-rw-rw-r-- 1 home home 387M Jun  2 01:15 cars_sales_gzip.parquet
-rw-rw-r-- 1 home home 269M Jun  2 01:14 cars_sales_brotli.parquet
-rw-rw-r-- 1 home home 250M Jun  2 01:15 cars_sales_zstd.parquet
```
### Кол-во строк в файле
```
./clickhouse local \
    -q "SELECT count() \
    FROM file('./datasets/raw_data/cars/cars_sales_zstd.parquet', Parquet)"
```
```
1294757
```
### Кол-во столбцов в файле
```
./clickhouse local \
    -q "DESCRIBE file('./datasets/raw_data/cars/cars_sales_zstd.parquet', Parquet)" \
    | wc -l
```
```
18
```
## Файл `Liquor_Sales.csv`
### Конвертируем `csv` в `parquet`
```
./clickhouse local \
    --max_memory_usage=2G \
    --max_threads=1 \
    --output_format_parquet_compression=zstd \
    -q "SELECT * FROM file('./datasets/raw_data/liquor/Liquor_Sales.csv', 'CSVWithNames') \
    INTO OUTFILE './datasets/raw_data/liquor/Liquor_Sales_zstd.parquet' FORMAT Parquet"
```
### Вывод статистики `/usr/bin/time -v`
```
	User time (seconds): 82.56
	System time (seconds): 8.52
	Percent of CPU this job got: 269%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:33.85
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 4143720
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 1082
	Minor (reclaiming a frame) page faults: 1499848
	Voluntary context switches: 25492
	Involuntary context switches: 4894
	Swaps: 0
	File system inputs: 9056560
	File system outputs: 1128056
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

### Размеры `parquet` файлов в зависимости от типа компрессии
```
ls -alhS datasets/raw_data/liquor | grep -v '^d' | xclip -sel clip
```
```
-rw-rw-r-- 1 home home 4.5G May 29 22:59 Liquor_Sales.csv
-rw-rw-r-- 1 home home 884M Jun  2 01:11 Liquor_Sales_none.parquet
-rw-rw-r-- 1 home home 679M Jun  2 01:12 Liquor_Sales_lz4.parquet
-rw-rw-r-- 1 home home 669M Jun  2 01:12 Liquor_Sales_snappy.parquet
-rw-rw-r-- 1 home home 556M Jun  2 01:10 Liquor_Sales_brotli.parquet
-rw-rw-r-- 1 home home 555M Jun  2 01:10 Liquor_Sales_gzip.parquet
-rw-rw-r-- 1 home home 551M Jun  2 01:11 Liquor_Sales_zstd.parquet
```

### Кол-во строк в файле
```
./clickhouse local \
    -q "SELECT count() \
    FROM file('./datasets/raw_data/liquor/Liquor_Sales_zstd.parquet', Parquet)"
```
```
19666763
```
### Кол-во столбцов в файле
```
./clickhouse local \
    -q "DESCRIBE file('./datasets/raw_data/liquor/Liquor_Sales_zstd.parquet', Parquet)" \
    | wc -l
```
```
24
```