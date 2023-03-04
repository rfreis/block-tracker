from aiohttp import ClientError

from app.celery import app as celery_app
from rate.utils import sync_rates


@celery_app.task(
    autoretry_for=(ClientError,), retry_backoff=True, retry_kwargs={"max_retries": 5}
)
def refresh_rates():
    sync_rates()
