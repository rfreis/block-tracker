from celery import shared_task

from rate.utils import sync_rates


@shared_task
def refresh_rates():
    sync_rates()
