#!/bin/bash
set -e

# Создаём пользователей с паролями из переменных окружения
# Проверяем существование '$AIRFLOW_DB_USER'
if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$AIRFLOW_DB_USER'" | grep -q 1; then
  psql -U "$POSTGRES_USER" -c "CREATE USER '$AIRFLOW_DB_USER' WITH PASSWORD '$AIRFLOW_DB_PASSWORD'"
  echo "User '$AIRFLOW_DB_USER' created"
else
  echo "User '$AIRFLOW_DB_USER' already exists"
fi

# Проверяем существование '$SUPERSET_DB_USER'
if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$SUPERSET_DB_USER'" | grep -q 1; then
  psql -U "$POSTGRES_USER" -c "CREATE USER '$SUPERSET_DB_USER' WITH PASSWORD '$SUPERSET_DB_PASSWORD'"
  echo "User '$SUPERSET_DB_USER' created"
else
  echo "User '$SUPERSET_DB_USER' already exists"
fi

# Создаём базы данных
if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_database WHERE datname='$AIRFLOW_DB_NAME'" | grep -q 1; then
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE DATABASE '$AIRFLOW_DB_NAME' OWNER '$AIRFLOW_DB_USER'"
else
  echo "DB '$AIRFLOW_DB_NAME' already exists"
fi

if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_database WHERE datname='$SUPERSET_DB_NAME'" | grep -q 1; then
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE DATABASE '$SUPERSET_DB_NAME' OWNER '$SUPERSET_DB_USER'"
else
  echo "DB '$SUPERSET_DB_NAME' already exists"
fi


# Настраиваем права
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" --d "$AIRFLOW_DB_NAME" <<-EOSQL
GRANT ALL PRIVILEGES ON SCHEMA public TO $AIRFLOW_DB_USER;
GRANT ALL ON ALL TABLES IN SCHEMA public TO $AIRFLOW_DB_USER;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO $AIRFLOW_DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $AIRFLOW_DB_USER;
EOSQL

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" --d "$SUPERSET_DB_NAME" <<-EOSQL
GRANT ALL PRIVILEGES ON SCHEMA public TO $SUPERSET_DB_USER;
GRANT ALL ON ALL TABLES IN SCHEMA public TO $SUPERSET_DB_USER;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO $SUPERSET_DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $SUPERSET_DB_USER;
EOSQL
