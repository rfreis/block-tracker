from app.celery import app as celery_app
from accounts.models import User
from dashboard.utils import sync_user_balance


@celery_app.task
def refresh_user_balances():
    users = User.objects.filter(is_active=True)
    for user in users:
        sync_user_balance(user)
