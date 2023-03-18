import logging
from calendar import monthrange
from datetime import date, datetime, timezone
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.db.models import Q

from dashboard.models import UserBalance
from rate.utils import get_usd_rate
from transaction.models import Transaction

logger = logging.getLogger(__name__)


def get_last_day(date_obj):
    last_day = monthrange(date_obj.year, date_obj.month)[1]
    return date(date_obj.year, date_obj.month, last_day)


def get_first_date(queryset):
    standard_start_date = get_last_day(date.today()) - relativedelta(years=1)
    if queryset:
        first_transaction_start_date = get_last_day(
            queryset.first().block_time - relativedelta(months=1)
        )
        if first_transaction_start_date < standard_start_date:
            return first_transaction_start_date
    return standard_start_date


def filter_transactions(queryset, date_reference, date_reference_month_before):
    queryset = queryset.filter(
        block_time__lte=datetime(
            date_reference.year,
            date_reference.month,
            date_reference.day,
            23,
            59,
            59,
            999999,
            tzinfo=timezone.utc,
        )
    )
    if date_reference_month_before:
        queryset = queryset.filter(
            block_time__gt=datetime(
                date_reference_month_before.year,
                date_reference_month_before.month,
                date_reference_month_before.day,
                23,
                59,
                59,
                999999,
                tzinfo=timezone.utc,
            )
        )
    return queryset


def get_balance_by_item_data(transaction, attr_name, user, balances):
    item_queryset = getattr(transaction, attr_name)
    item_queryset = item_queryset.filter(
        Q(address__user_wallet__user=user)
        | Q(address__extended_public_key__user_wallet__user=user)
    )
    for item in item_queryset:
        if attr_name == "inputdata":
            balances[item.asset_name] = str(
                Decimal(balances.get(item.asset_name, "0")) - Decimal(item.amount_asset)
            )
        else:
            balances[item.asset_name] = str(
                Decimal(balances.get(item.asset_name, "0")) + Decimal(item.amount_asset)
            )

    return balances


def sync_user_balance(user):
    logger.debug("Syncing UserBalance from user #%s" % user.id)
    queryset = (
        Transaction.objects.filter(
            is_orphan=False,
            is_confirmed=True,
        )
        .filter(
            Q(inputs__user_wallet__user=user)
            | Q(inputs__extended_public_key__user_wallet__user=user)
            | Q(outputs__user_wallet__user=user)
            | Q(outputs__extended_public_key__user_wallet__user=user)
        )
        .order_by("block_time")
        .distinct()
    )
    date_reference = get_first_date(queryset)
    date_reference_month_before = None
    last_balances = {}
    today = date.today()
    while date_reference <= get_last_day(today):
        transactions = filter_transactions(
            queryset,
            date_reference,
            date_reference_month_before,
        )
        for transaction in transactions:
            get_balance_by_item_data(
                transaction,
                "inputdata",
                user,
                last_balances,
            )
            get_balance_by_item_data(
                transaction,
                "outputdata",
                user,
                last_balances,
            )

        user_balance, _ = UserBalance.objects.get_or_create(
            user=user, date=date_reference
        )
        user_balance.balance = last_balances
        user_balance.save()

        date_reference_month_before = date_reference
        date_reference = get_last_day(date_reference + relativedelta(months=1))
    logger.debug("Synced UserBalance from user #%s" % user.id)


def get_or_create_last_user_balance(user, for_update=False):
    today = date.today()
    date_reference = get_last_day(today)
    user_balance, _ = UserBalance.objects.get_or_create(user=user, date=date_reference)
    if for_update:
        user_balance = UserBalance.objects.select_for_update().get(id=user_balance.id)
    return user_balance


def get_balance_rate(balances, time_reference):
    rate_balance = {}
    total = Decimal("0")
    for asset_name, amount_asset in balances.items():
        amount_usd = get_usd_rate(asset_name, amount_asset, time_reference)
        if amount_usd:
            rate_balance[asset_name] = amount_usd
            total += Decimal(amount_usd)
    return str(total), rate_balance
