DROP DATABASE IF EXISTS cars;

CREATE DATABASE IF NOT EXISTS cars;

CREATE TABLE IF NOT EXISTS cars.car_sales (
    brand Nullable(String),
    name Nullable(String),
    bodyType Nullable(String),
    color Nullable(String),
    fuelType Nullable(String),
    year Nullable(UInt32),
    mileage Nullable(UInt32),
    transmission Nullable(String),
    power Nullable(UInt16),
    price UInt32,
    vehicleConfiguration Nullable(String),
    engineName Nullable(String),
    engineDisplacement Nullable(Float64),
    date Date,
    location Nullable(String),
    link Nullable(String),
    description Nullable(String),
    parse_date DateTime
)
ENGINE = MergeTree()
ORDER BY (brand, date, parse_date)
SETTINGS allow_nullable_key = 1;

INSERT INTO cars.car_sales
SELECT
    nullIf(brand, '') as brand,
    nullIf(name, '') as name,
    nullIf(bodyType, '') as bodyType,
    nullIf(color, '') as color,
    nullIf(fuelType, '') as fuelType,
    toUInt32OrNull(toString(toFloat64OrNull(year))) as year,
    toUInt32OrNull(toString(toFloat64OrNull(mileage))) as mileage,
    nullIf(transmission, '') as transmission,
    toUInt32OrNull(toString(toFloat64OrNull(power))) as power,
    price,
    nullIf(vehicleConfiguration, '') as vehicleConfiguration,
    nullIf(engineName, '') as engineName,
    -- nullIf(engineDisplacement, '') as engineDisplacement,
    toFloat64OrNull(extract(engineDisplacement, '\\d+\\.?\\d*')) as engineDisplacement,
    parseDateTimeBestEffortUS(date) as date,
    nullIf(location, '') as location,
    nullIf(link, '') as link,
    nullIf(description, '') as description,
    parse_date
FROM file(
    '/var/lib/clickhouse/user_files/cars_sales.csv',
    'CSV',
    'brand String,
     name String,
     bodyType String,
     color String,
     fuelType String,
     year String,
     mileage String,
     transmission String,
     power String,
     price UInt32,
     vehicleConfiguration String,
     engineName String,
     engineDisplacement String,
     date String,
     location String,
     link String,
     description String,
     parse_date DateTime'
)
SETTINGS format_csv_delimiter = ',';
