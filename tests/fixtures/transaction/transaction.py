import pytest

from protocol.constants import CoinType
from transaction.models import Transaction


@pytest.fixture
@pytest.mark.usefixtures("db")
def transaction_fake_single_address_one(fake_single_address_one):
    transaction = Transaction.objects.create(
        address=fake_single_address_one,
        amount_usd="100.00",
        amount_coin="0.1",
        coin_type=CoinType.BTC,
        tx_id="fake_tx_id_one_for_single_address",
    )
    transaction.save()

    yield transaction

    transaction.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def transaction_fake_derived_address_one(fake_derived_address_one):
    transaction = Transaction.objects.create(
        address=fake_derived_address_one,
        amount_usd="500.00",
        amount_coin="0.5",
        coin_type=CoinType.BTC,
        tx_id="fake_tx_id_one_for_derived_address",
    )
    transaction.save()

    yield transaction

    transaction.delete()
