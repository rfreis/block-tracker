import pytest
from datetime import date, datetime, timezone
from freezegun import freeze_time

from dashboard.models import UserBalance
from dashboard.utils import sync_user_balance


@freeze_time("2022-6-01 12:10:00")
@pytest.mark.usefixtures(
    "db",
    "transactions_balance",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one",
)
def test_sync_user_balance(user_one):
    user_one_balances = UserBalance.objects.all()
    assert user_one_balances.count() == 0

    sync_user_balance(user_one)

    assert user_one_balances.count() == 13

    expected_balances = [
        [date(2021, 6, 30), {}],
        [date(2021, 7, 31), {}],
        [date(2021, 8, 31), {}],
        [date(2021, 9, 30), {}],
        [date(2021, 10, 31), {}],
        [date(2021, 11, 30), {}],
        [date(2021, 12, 31), {}],
        [date(2022, 1, 31), {"BTC": "0.25"}],
        [date(2022, 2, 28), {"BTC": "0.35"}],
        [date(2022, 3, 31), {"BTC": "0.35"}],
        [date(2022, 4, 30), {"BTC": "0.35"}],
        [date(2022, 5, 31), {"BTC": "3.85"}],
        [date(2022, 6, 30), {"BTC": "3.85"}],
    ]
    balances = []
    for user_balance in user_one_balances:
        balances.append([user_balance.date, user_balance.balance])

    assert expected_balances == balances


@freeze_time("2022-6-01 12:10:00")
@pytest.mark.usefixtures(
    "db",
    "transactions_balance",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one_user_two",
)
def test_sync_user_balance_multiple_users(user_one, user_two):
    assert UserBalance.objects.all().count() == 0

    sync_user_balance(user_one)
    sync_user_balance(user_two)

    user_one_balances = UserBalance.objects.filter(user=user_one)
    user_two_balances = UserBalance.objects.filter(user=user_two)
    assert user_one_balances.count() == 13
    assert user_two_balances.count() == 13

    expected_balances = {
        "user_one": [
            [date(2021, 6, 30), {}],
            [date(2021, 7, 31), {}],
            [date(2021, 8, 31), {}],
            [date(2021, 9, 30), {}],
            [date(2021, 10, 31), {}],
            [date(2021, 11, 30), {}],
            [date(2021, 12, 31), {}],
            [date(2022, 1, 31), {}],
            [date(2022, 2, 28), {}],
            [date(2022, 3, 31), {}],
            [date(2022, 4, 30), {}],
            [date(2022, 5, 31), {"BTC": "1"}],
            [date(2022, 6, 30), {"BTC": "1"}],
        ],
        "user_two": [
            [date(2021, 6, 30), {}],
            [date(2021, 7, 31), {}],
            [date(2021, 8, 31), {}],
            [date(2021, 9, 30), {}],
            [date(2021, 10, 31), {}],
            [date(2021, 11, 30), {}],
            [date(2021, 12, 31), {}],
            [date(2022, 1, 31), {"BTC": "0.25"}],
            [date(2022, 2, 28), {"BTC": "0.35"}],
            [date(2022, 3, 31), {"BTC": "0.35"}],
            [date(2022, 4, 30), {"BTC": "0.35"}],
            [date(2022, 5, 31), {"BTC": "2.85"}],
            [date(2022, 6, 30), {"BTC": "2.85"}],
        ],
    }
    balances = {"user_one": [], "user_two": []}
    for user_balance in user_one_balances:
        balances["user_one"].append([user_balance.date, user_balance.balance])
    for user_balance in user_two_balances:
        balances["user_two"].append([user_balance.date, user_balance.balance])

    assert expected_balances["user_one"] == balances["user_one"]
    assert expected_balances["user_two"] == balances["user_two"]


@freeze_time("2022-6-01 12:10:00")
@pytest.mark.usefixtures(
    "db",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one",
)
def test_sync_user_balance_with_older_balances(transactions_balance, user_one):
    transaction_1 = transactions_balance[0]
    transaction_1.block_time = datetime(2021, 4, 30, 12, 00, tzinfo=timezone.utc)
    transaction_1.save()
    UserBalance.objects.create(
        date=date(2021, 4, 30),
        balance={"BTC": "0.25"},
        user=user_one,
    )
    user_one_balances = UserBalance.objects.all()
    assert user_one_balances.count() == 1

    sync_user_balance(user_one)

    assert user_one_balances.count() == 16

    expected_balances = [
        [date(2021, 3, 31), {}],
        [date(2021, 4, 30), {"BTC": "0.25"}],
        [date(2021, 5, 31), {"BTC": "0.25"}],
        [date(2021, 6, 30), {"BTC": "0.25"}],
        [date(2021, 7, 31), {"BTC": "0.25"}],
        [date(2021, 8, 31), {"BTC": "0.25"}],
        [date(2021, 9, 30), {"BTC": "0.25"}],
        [date(2021, 10, 31), {"BTC": "0.25"}],
        [date(2021, 11, 30), {"BTC": "0.25"}],
        [date(2021, 12, 31), {"BTC": "0.25"}],
        [date(2022, 1, 31), {"BTC": "0.25"}],
        [date(2022, 2, 28), {"BTC": "0.35"}],
        [date(2022, 3, 31), {"BTC": "0.35"}],
        [date(2022, 4, 30), {"BTC": "0.35"}],
        [date(2022, 5, 31), {"BTC": "3.85"}],
        [date(2022, 6, 30), {"BTC": "3.85"}],
    ]
    balances = []
    for user_balance in user_one_balances:
        balances.append([user_balance.date, user_balance.balance])

    assert expected_balances == balances
