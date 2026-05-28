class TableNotSetError(ValueError):
    """Исключение для случая, когда таблица не установлена."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Table is not set"
        super().__init__(message)


class DBNotSetError(ValueError):
    """Исключение для случая, когда db не установлена."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "DB is not set"
        super().__init__(message)
