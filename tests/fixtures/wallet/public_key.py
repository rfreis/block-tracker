import pytest

from protocol.constants import ProtocolType
from wallet.models import PublicKey


@pytest.fixture
@pytest.mark.usefixtures("db")
def fake_public_key_one():
    public_key = PublicKey.objects.create(
        hash="any_hash",
        protocol_type=ProtocolType.BITCOIN,
    )
    public_key.save()

    yield public_key

    public_key.delete()
