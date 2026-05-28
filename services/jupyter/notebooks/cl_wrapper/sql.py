"""SQL."""

import pandas as pd
from clickhouse_connect.driver.client import Client
from clickhouse_connect.driver.query import QueryResult

from .my_exceptions import DBNotSetError, TableNotSetError


class SQLBase:
    """SQL."""

    def __init__(self, db: str | None = None, table: str | None = None) -> None:
        """Init.

        :param db: _description_, defaults to None
        :type db: str | None, optional
        :param table: _description_, defaults to None
        :type table: str | None, optional
        """
        self._db: str | None = db
        self._table: str | None = table

    @property
    def db(self) -> str | None:
        if self._db is not None:
            return self._db
        raise DBNotSetError

    @db.setter
    def db(self, db: str) -> None:
        self._db = db

    @property
    def table(self) -> str | None:
        if self._table is not None:
            return self._table
        raise TableNotSetError

    @table.setter
    def table(self, table: str) -> None:
        self._table = table


class SQL(SQLBase):
    """SQL."""

    def __init__(
        self, client: Client, db: str | None = None, table: str | None = None
    ) -> None:
        """Init.

        :param conn: _description_
        :type conn: Client
        :param db: _description_, defaults to None
        :type db: str | None, optional
        :param table: _description_, defaults to None
        :type table: str | None, optional
        """
        self.client = client

        self.sql = None
        super().__init__(db=db, table=table)

    def set_db(self, db: str) -> "SQL":
        """Set DB."""
        self.db = db
        return self

    def set_table(self, table: str) -> "SQL":
        """Set Table."""
        self.table = table
        return self

    def query(self) -> QueryResult:
        """Get SQL Result as Clickhouse QueryResult.

        :return: _description_
        :rtype: QueryResult
        """
        return self.client.query(query=self.sql)

    def query_df(self) -> pd.DataFrame:
        """Get SQL Result as pd.DataFrame.

        :return: _description_
        :rtype: pd.DataFrame
        """
        return self.client.query_df(query=self.sql)

    def get_total(self) -> "SQL":
        """Get Total Rows.

        :return: _description_
        :rtype: SQL
        """
        self.sql = f"SELECT COUNT(*) FROM {self.db}.{self.table}"  # noqa: S608
        return self

    def get_describe_table(self) -> "SQL":
        """Get Describe Table.

        :return: _description_
        :rtype: SQL
        """
        self.sql = f"DESCRIBE TABLE {self.db}.{self.table}"
        return self

    def get_count_column_is_not_null(self, column: str) -> "SQL":
        """Get Count column is Not Null.

        :return: _description_
        :rtype: SQL
        """
        self.sql = f"""SELECT count(*)
        FROM {self.db}.{self.table}
        WHERE {column} IS NOT NULL"""  # noqa: S608
        return self

    def get_samples(
        self,
        *,
        cars_columns: list[str],
        sample_count: int = 3,
        sample_size: int = 1000,
    ) -> "SQL":
        """Get samples."""
        self.sql = f"""
        WITH ranked AS (
            SELECT
                {",".join(cars_columns)},
                NTILE({sample_count}) OVER (ORDER BY rand()) AS tile
            FROM cars.car_sales
        ),
        ranked_with_row_num AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY tile ORDER BY rand()) AS row_num
            FROM ranked
        )
        SELECT *
        FROM ranked_with_row_num
        WHERE row_num <= {sample_size}
        ORDER BY tile, rand()
        """  # noqa: S608
        return self
