import os

from celery import Celery
from celery.signals import setup_logging

__all__ = ["app"]


SETTINGS_MODULE_PATH = os.environ.get("SETTINGS_MODULE_PATH", "app.settings.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE_PATH)


app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from django.conf import settings  # noqa: F401


app.autodiscover_tasks()
