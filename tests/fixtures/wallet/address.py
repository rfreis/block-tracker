import pytest

from tests.fixtures.utils import delete_related_obj

from protocol.constants import ProtocolType
from wallet.models import Address


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_one(hash_address_p2pkh_bitcoin_three):
    address = Address.objects.create(
        hash=hash_address_p2pkh_bitcoin_three,
        protocol_type=ProtocolType.BITCOIN,
    )

    yield address

    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_two(hash_address_p2pkh_bitcoin_two):
    address = Address.objects.create(
        hash=hash_address_p2pkh_bitcoin_two,
        protocol_type=ProtocolType.BITCOIN,
    )

    yield address

    delete_related_obj(address)
    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def derived_bitcoin_address_one(
    xpublic_key_bitcoin_one, hash_address_p2wpkh_bitcoin_one
):
    address = Address.objects.create(
        extended_public_key=xpublic_key_bitcoin_one,
        hash=hash_address_p2wpkh_bitcoin_one,
        protocol_type=xpublic_key_bitcoin_one.protocol_type,
        is_change=False,
        index=0,
    )

    yield address

    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def derived_bitcoin_address_two(
    xpublic_key_bitcoin_one, hash_address_p2wpkh_bitcoin_two
):
    address = Address.objects.create(
        extended_public_key=xpublic_key_bitcoin_one,
        hash=hash_address_p2wpkh_bitcoin_two,
        protocol_type=xpublic_key_bitcoin_one.protocol_type,
        is_change=False,
        index=1,
    )

    yield address

    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def derived_bitcoin_address_three(
    xpublic_key_bitcoin_two, hash_address_p2pkh_bitcoin_two
):
    address = Address.objects.create(
        extended_public_key=xpublic_key_bitcoin_two,
        hash=hash_address_p2pkh_bitcoin_two,
        protocol_type=xpublic_key_bitcoin_two.protocol_type,
        is_change=False,
        index=24,
    )

    yield address

    address.delete()
