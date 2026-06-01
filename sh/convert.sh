#!/bin/bash

dataset_cars="../datasets/raw_data/cars/cars_sales.csv"
dataset_liquor="../datasets/raw_data/liquor/Liquor_Sales.csv"

ParquetCompression=("brotli" "gzip" "none" "zstd" "lz4" "snappy")

for Compression in "${ParquetCompression[@]}"
do
    echo "Convert cars_sales.csv to parquet with $Compression compression"
    ./clickhouse local --max_memory_usage=2G --max_threads=1 --output_format_parquet_compression=$Compression -q "SELECT * FROM file ('./datasets/raw_data/cars/cars_sales.csv', CSVWithNames) INTO OUTFILE './datasets/raw_data/cars/cars_sales_$Compression.parquet' FORMAT Parquet"
done