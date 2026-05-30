DROP DATABASE IF EXISTS cars;

CREATE DATABASE IF NOT EXISTS cars;

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
    -- engineDisplacement_type Nullable(String),
    date Date,
    location LowCardinality(Nullable(String)),
    -- link Nullable(String),
    -- description Nullable(String),
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
    toUInt32OrNull(toString(toFloat32OrNull(power))) as power,
    price,
    nullIf(vehicleConfiguration, '') as vehicleConfiguration,

    if(
        vehicleConfiguration IS NULL,
        NULL,
        vehicleConfiguration LIKE '%AWD%'
    ) AS has_awd,


    nullIf(engineName, '') as engineName,
    toFloat32OrNull(extract(engineDisplacement, '\\d+\\.?\\d*')) as engineVolume,
    -- nullIf(extract(engineDisplacement, '([A-Za-z]+)$'),'') AS engineDisplacement_type,
    parseDateTimeBestEffortUS(date) as date,
    nullIf(location, '') as location,
    -- nullIf(link, '') as link,
    -- nullIf(description, '') as description,
    parse_date
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
