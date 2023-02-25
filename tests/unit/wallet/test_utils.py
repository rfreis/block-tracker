import pytest
from freezegun import freeze_time

from django.db import transaction as db_transaction

from wallet.models import Address
from wallet.utils import (
    derive_addresses_from_extended_public_key,
    get_last_address_index_from_extended_public_key,
    update_all_balances,
)


@pytest.mark.usefixtures(
    "db", "derived_bitcoin_address_one", "derived_bitcoin_address_two"
)
def test_get_last_address_index_from_xpublic_key(xpublic_key_bitcoin_one):
    last_index = get_last_address_index_from_extended_public_key(
        xpublic_key_bitcoin_one
    )
    assert last_index == 1


@pytest.mark.usefixtures("db")
def test_derive_addresses_from_extended_public_key(xpublic_key_bitcoin_one):
    queryset = Address.objects.filter(extended_public_key=xpublic_key_bitcoin_one)

    assert queryset.count() == 0

    derive_addresses_from_extended_public_key(xpublic_key_bitcoin_one)

    assert queryset.filter(details__semantic="P2PKH", is_change=False).count() == 21
    assert queryset.filter(details__semantic="P2WPKH", is_change=False).count() == 21
    assert queryset.filter(details__semantic="P2PKH", is_change=True).count() == 21
    assert queryset.filter(details__semantic="P2WPKH", is_change=True).count() == 21


@freeze_time("2022-12-01 12:00:00")
@pytest.mark.usefixtures(
    "db",
    "user_one",
    "user_wallet_bitcoin_xpub_one",
    "user_wallet_single_bitcoin_address_one",
)
def test_update_all_balances(
    derived_bitcoin_address_one,
    derived_bitcoin_address_two,
    single_bitcoin_address_one,
    user_balance_two_empty,
):
    with db_transaction.atomic():
        update_all_balances(
            derived_bitcoin_address_one,
            "BTC",
            "0.25",
            "outputdata",
        )
        update_all_balances(
            derived_bitcoin_address_one,
            "BTC",
            "0.5",
            "outputdata",
        )
        update_all_balances(
            derived_bitcoin_address_one,
            "BTC",
            "0.4",
            "inputdata",
        )

    derived_bitcoin_address_one.refresh_from_db()
    derived_bitcoin_address_one.extended_public_key.refresh_from_db()
    user_balance_two_empty.refresh_from_db()

    assert derived_bitcoin_address_one.balance["BTC"] == "0.35"
    assert derived_bitcoin_address_one.extended_public_key.balance["BTC"] == "0.35"
    assert user_balance_two_empty.balance["BTC"] == "0.35"

    with db_transaction.atomic():
        update_all_balances(
            derived_bitcoin_address_two,
            "BTC",
            "2.5",
            "outputdata",
        )
        update_all_balances(
            single_bitcoin_address_one,
            "BTC",
            "1",
            "outputdata",
        )

    derived_bitcoin_address_one.refresh_from_db()
    derived_bitcoin_address_one.extended_public_key.refresh_from_db()
    user_balance_two_empty.refresh_from_db()
    derived_bitcoin_address_two.refresh_from_db()
    single_bitcoin_address_one.refresh_from_db()

    assert derived_bitcoin_address_one.balance["BTC"] == "0.35"
    assert derived_bitcoin_address_two.balance["BTC"] == "2.50"
    assert derived_bitcoin_address_one.extended_public_key.balance["BTC"] == "2.85"
    assert single_bitcoin_address_one.balance["BTC"] == "1.0"
    assert user_balance_two_empty.balance["BTC"] == "3.85"
