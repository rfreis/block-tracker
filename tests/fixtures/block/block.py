import pytest

from protocol.constants import ProtocolType
from block.models import Block


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761592_confirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761592,
        block_hash=block_hashes_by_id[761592],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )

    yield block

    block.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761593_unconfirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761593,
        block_hash=block_hashes_by_id[761593],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )

    yield block

    block.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761594_unconfirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761594,
        block_hash=block_hashes_by_id[761594],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )

    yield block

    block.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761595_unconfirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761595,
        block_hash=block_hashes_by_id[761595],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )

    yield block

    block.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761596_unconfirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761596,
        block_hash=block_hashes_by_id[761596],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )

    yield block

    block.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def block_bitcoin_761597_unconfirmed(block_hashes_by_id):
    block = Block.objects.create(
        block_id=761597,
        block_hash=block_hashes_by_id[761597],
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )

    yield block

    block.delete()
