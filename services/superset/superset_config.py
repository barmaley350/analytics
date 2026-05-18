SECRET_KEY = "2d9fd294aa390df0360036992ded4db6c30a962a3b05375c05a4e438ea40e433"
PREVENT_UNSAFE_DB_CONNECTIONS = False
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
