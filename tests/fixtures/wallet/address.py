import pytest

from protocol.constants import ProtocolType
from wallet.models import Address


@pytest.fixture
@pytest.mark.usefixtures("db")
def fake_single_address_one():
    address = Address.objects.create(
        hash="any_single_hash",
        protocol_type=ProtocolType.BITCOIN,
    )
    address.save()

    yield address

    address.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def fake_derived_address_one(fake_public_key_one):
    address = Address.objects.create(
        public_key=fake_public_key_one,
        hash="any_derived_hash_0",
        protocol_type=fake_public_key_one.protocol_type,
        is_change=False,
        index=0,
    )
    address.save()

    yield address

    address.delete()
