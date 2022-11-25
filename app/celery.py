import os

from celery import Celery


__all__ = ["app"]


SETTINGS_MODULE_PATH = os.environ.get("SETTINGS_MODULE_PATH", "app.settings.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE_PATH)


BROKER_URL = os.environ.get("CELERY_BROKER", "")


app = Celery("backend", broker=BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
