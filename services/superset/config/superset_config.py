import os
from urllib.parse import quote_plus

from celery.schedules import crontab
from superset.tasks.types import FixedExecutor  # type: ignore

DB_TYPE = os.getenv("SUPERSET_DB_TYPE", "postgresql")
DB_DRIVER = os.getenv("SUPERSET_DB_DRIVER", "psycopg2")
DB_HOST = os.getenv("SUPERSET_DB_HOST", "localhost")
DB_PORT = os.getenv("SUPERSET_DB_PORT", "5432")
DB_NAME = os.getenv("SUPERSET_DB_NAME", "superset_metadata")
DB_USER = os.getenv("SUPERSET_DB_USER", "superset_user")
DB_PASSWORD = os.getenv("SUPERSET_DB_PASSWORD", "")
DB_SSL_MODE = os.getenv("SUPERSET_DB_SSL_MODE", "prefer")
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "")
CELERY_BROKER_URL = os.getenv("SUPERSET_CELERY_BROKER_URL", "")

PREVENT_UNSAFE_DB_CONNECTIONS = False

# Формируем строку подключения
if DB_TYPE == "postgresql":
    encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+{DB_DRIVER}://{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSL_MODE}"
    )
    CELERY_RESULT_BACKEND = (
        f"db+postgresql+{DB_DRIVER}://{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSL_MODE}"
    )
else:
    # Fallback на SQLite, если тип БД не распознан
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/database/superset.db"
    CELERY_RESULT_BACKEND = "sqlite:////app/database/superset.db"


FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DRILL_TO_DETAIL": True,
    "ALERT_REPORTS": True,
    "DATE_FORMAT_IN_EMAIL_SUBJECT": True,
    "PLAYWRIGHT_REPORTS_AND_THUMBNAILS": True,
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
SMTP_MAIL_FROM = "report@analytics.com"  # email отправителя

ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
ALERT_REPORTS_EXECUTORS = [FixedExecutor("admin")]
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset Report] "


# Celery configuration
class CeleryConfig:  # noqa: D101
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
    imports = (
        "superset.sql_lab",
        "superset.tasks",
        "superset.tasks.thumbnails",
    )
    task_annotations = {  # noqa: RUF012
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": 120,
            "soft_time_limit": 150,
            "ignore_result": True,
        },
    }
    worker_prefetch_multiplier = 10
    task_acks_late = True
    task_protocol = 1
    worker_prefetch_enabled = False

    # Добавляем расписание для планировщика отчётов
    beat_schedule = {  # noqa: RUF012
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*/5"),
        },
    }


CELERY_CONFIG = CeleryConfig

PLAYWRIGHT_REPORTS_AND_THUMBNAILS = True
WEBDRIVER_BASEURL = "http://service.superset:8088"
WEBDRIVER_BASEURL_USER_FRIENDLY = "http://localhost:8088"

