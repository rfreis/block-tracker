import pytest  # noqa: F401

from protocol.constants import ProtocolType
from tests.fixtures.utils import delete_related_obj
from wallet.models import ExtendedPublicKey


@pytest.fixture
@pytest.mark.usefixtures("db")
def xpublic_key_bitcoin_one(hash_xpub_bitcoin_one):
    xpublic_key = ExtendedPublicKey.objects.create(
        hash=hash_xpub_bitcoin_one,
        protocol_type=ProtocolType.BITCOIN,
        balance={"BTC": "0.0"},
    )

    yield xpublic_key

    delete_related_obj(xpublic_key)
    xpublic_key.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def xpublic_key_bitcoin_two(hash_xpub_bitcoin_two):
    xpublic_key = ExtendedPublicKey.objects.create(
        hash=hash_xpub_bitcoin_two,
        protocol_type=ProtocolType.BITCOIN,
    )

    yield xpublic_key

    delete_related_obj(xpublic_key)
    xpublic_key.delete()
