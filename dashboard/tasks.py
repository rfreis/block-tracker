from celery import shared_task

from accounts.models import User
from dashboard.utils import sync_user_balance


@shared_task
def refresh_user_balances():
    users = User.objects.filter(is_active=True)
    for user in users:
        sync_user_balance(user)
