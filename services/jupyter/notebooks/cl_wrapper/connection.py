import clickhouse_connect
from clickhouse_connect.driver.client import Client


class Connection:
    def __init__(
        self,
        *,
        host: str = "localhost",
        port: int = 8123,
        username: str = "default",
        password: str = "",
    ):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._client: Client | None = None

    def connect(self) -> Client:
        """Устанавливает соединение с ClickHouse."""
        try:
            self._client = clickhouse_connect.get_client(
                host=self._host,
                port=self._port,
                username=self._username,
                password=self._password,
            )
        except Exception as e:
            raise ConnectionError(e) from e
        else:
            return self._client

    def disconnect(self) -> str:
        """Закрывает соединение, если оно существует."""
        if self._client is not None:
            self._client.close()
            self._client = None
            return "Соединение закрыто"
        return "Соединение не было установлено"

    def check_connection(self) -> bool:
        """Проверяет активность соединения.

        Проверяет активность соединения через запрос SELECT 1.
        Возвращает True, если соединение работает, иначе False.
        """
        if self._client is None:
            return False
        try:
            self._client.query("SELECT 1")
        except ConnectionError:
            return False
        else:
            return True

    def get_connection(self) -> Client | None:
        """Возвращает активное соединение.

        Возвращает активное соединение. Если соединения нет — создаёт новое.
        """
        if not self.check_connection():
            self.connect()
        return self._client
