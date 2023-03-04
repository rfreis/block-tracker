import logging

from app.celery import app as celery_app
from accounts.models import User
from crm.utils import send_confirmed_transaction
from dashboard.utils import sync_user_balance
from protocol.utils.exceptions import ClientException
from wallet.models import Address, ExtendedPublicKey
from transaction.models import Transaction
from transaction.utils import (
    sync_transactions_from_address,
    sync_transactions_from_extended_public_key,
)


logger = logging.getLogger(__name__)


def get_users_from_addresses(addresses):
    users = set()
    for address in addresses:
        for user_wallet in address.user_wallet.all():
            users.add(user_wallet.user)
        if address.extended_public_key:
            for user_wallet in address.extended_public_key.user_wallet.all():
                users.add(user_wallet.user)
    return users


@celery_app.task
def new_confirmed_transactions(transaction_ids):
    transactions = Transaction.objects.filter(
        id__in=transaction_ids,
        is_confirmed=True,
    )
    for transaction in transactions:
        users = set()
        users = users.union(get_users_from_addresses(transaction.inputs.all()))
        users = users.union(get_users_from_addresses(transaction.outputs.all()))
        for user in users:
            send_confirmed_transaction(user, transaction)


@celery_app.task(
    autoretry_for=(ClientException,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def new_address(address_id):
    address = Address.objects.get(id=address_id)
    sync_transactions_from_address(address)
    users = User.objects.filter(user_wallet__address=address)
    for user in users:
        sync_user_balance(user)


@celery_app.task(
    autoretry_for=(ClientException,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def new_extended_public_key(extended_public_key_id):
    extended_public_key = ExtendedPublicKey.objects.get(id=extended_public_key_id)
    sync_transactions_from_extended_public_key(extended_public_key)
    users = User.objects.filter(user_wallet__extended_public_key=extended_public_key)
    for user in users:
        sync_user_balance(user)
