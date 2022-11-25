import pytest

from wallet.models import Address
from wallet.utils import (
    derive_addresses_from_extended_public_key,
    get_last_address_index_from_extended_public_key,
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
