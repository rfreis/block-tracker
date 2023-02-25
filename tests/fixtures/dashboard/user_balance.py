import pytest
from datetime import date

from dashboard.models import UserBalance


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_balance_one(user_one):
    user_balance = UserBalance.objects.create(
        user=user_one,
        date=date(2023, 1, 31),
        balance={"BTC": "0.5", "BTCTEST": "0.2"},
    )

    yield user_balance

    user_balance.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_balance_two_empty(user_one):
    user_balance = UserBalance.objects.create(
        user=user_one,
        date=date(2022, 12, 31),
        balance={},
    )

    yield user_balance

    user_balance.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_balance_history(user_one):
    user_balances = [
        UserBalance(
            user=user_one,
            date=date(2022, 1, 31),
            balance={},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 2, 28),
            balance={},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 3, 31),
            balance={},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 4, 30),
            balance={},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 5, 31),
            balance={"BTC": "0.5"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 6, 30),
            balance={"BTC": "0.5"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 7, 31),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 8, 31),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 9, 30),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 10, 31),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 11, 30),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
        UserBalance(
            user=user_one,
            date=date(2022, 12, 31),
            balance={"BTC": "0.5", "BTCTEST": "0.2"},
        ),
    ]
    user_balances = UserBalance.objects.bulk_create(user_balances)

    yield user_balances

    for user_balance in user_balances:
        user_balance.delete()
