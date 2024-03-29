import pytest  # noqa: F401

from protocol.constants import ProtocolType
from tests.fixtures.utils import delete_related_obj
from wallet.models import Address


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_one(hash_address_p2pkh_bitcoin_three):
    address = Address.objects.create(
        hash=hash_address_p2pkh_bitcoin_three,
        protocol_type=ProtocolType.BITCOIN,
        balance={"BTC": "0.0"},
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
def single_bitcoin_address_three():
    address = Address.objects.create(
        hash="14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer",
        protocol_type=ProtocolType.BITCOIN,
    )

    yield address

    delete_related_obj(address)
    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_four():
    address = Address.objects.create(
        hash="1Dn274qviAhHXgq4e8Y5XmaBsnjhAB9GR8",
        protocol_type=ProtocolType.BITCOIN,
    )

    yield address

    delete_related_obj(address)
    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_five():
    address = Address.objects.create(
        hash="1Fog84w3gEYkyDN6oaWaXbLuFqEF93uMho",
        protocol_type=ProtocolType.BITCOIN,
    )

    yield address

    delete_related_obj(address)
    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def single_bitcoin_address_six():
    address = Address.objects.create(
        hash="1FGnQpZ1fYT4x3dzqtx1F21Y1TBGbumegi",
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
        details={"semantic": "P2PKH"},
    )

    yield address

    delete_related_obj(address)
    address.delete()
