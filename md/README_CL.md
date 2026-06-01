# Работа с `clickhouse-local`
## Конвертируем файл из `csv` в `parquet`
Для ускорения работы с локальным файлом его нужно конвертировать из `csv` в `parquet`

> [!NOTE]
> Используйте `--max_memory_usage=2G` и `--max_threads=1` для слабых компьютеров

## Файл `cars_sales.csv`
### Конвертируем `csv` в `parquet`
```
./clickhouse local --max_memory_usage=2G --max_threads=1 -q "SELECT * FROM file ('./datasets/raw_data/cars/cars_sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/cars/cars_sales.parquet' FORMAT Parquet"
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
### Размеры файлов 
```
ls -alhS datasets/raw_data/cars | grep -v '^d' | xclip -sel clip
```
```
-rw-rw-r-- 1 home home 2.0G May 20 08:55 cars_sales.csv
-rw-rw-r-- 1 home home 250M Jun  1 21:13 cars_sales.parquet
```
### Кол-во сток в файле
```
./clickhouse local -q "SELECT count() FROM file('./datasets/raw_data/cars/cars_sales.parquet', Parquet)"
```
```
1294757
```
### Кол-во столбцов в файле
```
./clickhouse local -q "DESCRIBE file('./datasets/raw_data/cars/cars_sales.parquet', Parquet)" | wc -l
```
```
18
```
## Файл `Liquor_Sales.csv`
### Конвертируем `csv` в `parquet`
```
./clickhouse local --max_memory_usage=2G --max_threads=1 -q "SELECT * FROM file ('./datasets/raw_data/liquor/Liquor_Sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/liquor/Liquor_Sales.parquet' FORMAT Parquet"
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

### Размеры файлов
```
ls -alhS datasets/raw_data/liquor | grep -v '^d' | xclip -sel clip
```
```
-rw-rw-r-- 1 home home 4.5G May 29 22:59 Liquor_Sales.csv
-rw-rw-r-- 1 home home 551M Jun  1 21:29 Liquor_Sales.parquet
```

### Кол-во сток в файле
```
./clickhouse local -q "SELECT count() FROM file('./datasets/raw_data/liquor/Liquor_Sales.parquet', Parquet)"
```
```
19666763
```
### Кол-во столбцов в файле
```
./clickhouse local -q "DESCRIBE file('./datasets/raw_data/liquor/Liquor_Sales.parquet', Parquet)" | wc -l
```
```
24
```