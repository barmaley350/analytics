#!/bin/bash

datasets=("./datasets/raw_data/cars/cars_sales.csv" "./datasets/raw_data/liquor/Liquor_Sales.csv")


ParquetCompression=("brotli" "gzip" "none" "zstd" "lz4" "snappy")

for dataset in "${datasets[@]}"; do
    dataset_path=$(dirname "$dataset")
    dataset_name=$(basename "$dataset")
    dataset_name_template="${dataset_name%.*}"
   
    for Compression in "${ParquetCompression[@]}"; do
        echo "Convert $dataset_name to parquet with $Compression compression"
        ./clickhouse local \
            --max_memory_usage=2G \
            --max_threads=1 \
            --output_format_parquet_compression="$Compression" \
            -q "SELECT * FROM file('$dataset', 'CSVWithNames') \
            INTO OUTFILE '${dataset_path}/${dataset_name_template}_${Compression}.parquet' FORMAT Parquet"
    done
done