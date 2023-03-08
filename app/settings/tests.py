# flake8: noqa
from .base import *

default_db_name = DATABASES["default"]["NAME"]
DATABASES["default"]["NAME"] = f"test_{default_db_name}"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "webmaster@example.com"

CELERY_BROKER_URL = ""
CELERY_RESULT_BACKEND = ""
