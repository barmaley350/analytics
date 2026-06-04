import os
from urllib.parse import quote_plus

DB_TYPE = os.getenv("SUPERSET_DB_TYPE", "postgresql")
DB_DRIVER = os.getenv("SUPERSET_DB_DRIVER", "psycopg2")
DB_HOST = os.getenv("SUPERSET_DB_HOST", "localhost")
DB_PORT = os.getenv("SUPERSET_DB_PORT", "5432")
DB_NAME = os.getenv("SUPERSET_DB_NAME", "superset_metadata")
DB_USER = os.getenv("SUPERSET_DB_USER", "superset_user")
DB_PASSWORD = os.getenv("SUPERSET_DB_PASSWORD", "")
DB_SSL_MODE = os.getenv("SUPERSET_DB_SSL_MODE", "prefer")
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "")

PREVENT_UNSAFE_DB_CONNECTIONS = False

# Формируем строку подключения
if DB_TYPE == "postgresql":
    encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+{DB_DRIVER}://{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSL_MODE}"
    )
else:
    # Fallback на SQLite, если тип БД не распознан
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/database/superset.db"

print("SQLALCHEMY_DATABASE_URI", SQLALCHEMY_DATABASE_URI)

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DRILL_TO_DETAIL": True,
    "ALERT_REPORTS": True,
    "DATE_FORMAT_IN_EMAIL_SUBJECT": True,
}


LANGUAGES = {
    "ru": {"flag": "ru", "name": "Русский"},
    "en": {"flag": "us", "name": "English"},
}

BABEL_DEFAULT_LOCALE = "en"

SMTP_HOST = "service.smtp4dev"  # адрес SMTP‑сервера
SMTP_PORT = 25  # порт (обычно 587 для STARTTLS, 465 для SSL)
SMTP_STARTTLS = True  # использовать STARTTLS
SMTP_SSL = False  # использовать SSL (если SMTP_STARTTLS=False)
SMTP_USER = ""  # логин (может быть пустым для неаутентифицированного SMTP)
SMTP_PASSWORD = ""  # пароль (может быть пустым)
SMTP_MAIL_FROM = "noreply@example.com"  # email отправителя

ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset Report] "
