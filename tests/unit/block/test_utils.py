import pytest
from datetime import datetime, timezone
from decimal import Decimal
import logging

from block.models import Block
from block.utils import (
    check_orphan_blocks,
    confirm_blocks,
    digest_new_block,
    sync_chain_of_blocks,
)
from protocol.bitcoin.backend_blockbook import BLOCKBOOK_SETTINGS
from protocol.constants import ProtocolType
from transaction.models import Transaction
from wallet.models import Address


@pytest.mark.usefixtures("db")
def test_check_orphan_blocks(
    aioresponses, block_bitcoin_761592_confirmed, block_bitcoin_761593_unconfirmed
):
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761593",
            payload={"blockHash": block_bitcoin_761593_unconfirmed.block_hash},
        )
        check_orphan_blocks(ProtocolType.BITCOIN)

    block_bitcoin_761592_confirmed.refresh_from_db()
    block_bitcoin_761593_unconfirmed.refresh_from_db()
    assert block_bitcoin_761592_confirmed.is_orphan == False
    assert block_bitcoin_761593_unconfirmed.is_orphan == False


@pytest.mark.usefixtures("db")
def test_check_orphan_blocks_orphaned(
    aioresponses, block_bitcoin_761592_confirmed, block_bitcoin_761593_unconfirmed
):
    transaction = Transaction.objects.create(
        protocol_type=ProtocolType.BITCOIN, block_id=761593
    )
    assert transaction.is_orphan == False

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761592",
            payload={"blockHash": block_bitcoin_761592_confirmed.block_hash},
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761593",
            payload={"blockHash": "a different hash"},
        )
        check_orphan_blocks(ProtocolType.BITCOIN)

    block_bitcoin_761592_confirmed.refresh_from_db()
    block_bitcoin_761593_unconfirmed.refresh_from_db()
    assert block_bitcoin_761592_confirmed.is_orphan == False
    assert block_bitcoin_761593_unconfirmed.is_orphan == True
    transaction.refresh_from_db()
    assert transaction.is_orphan == True


@pytest.mark.usefixtures("db")
def test_check_orphan_blocks_confirmed_orphan(
    caplog,
    aioresponses,
    block_bitcoin_761592_confirmed,
    block_bitcoin_761593_unconfirmed,
):
    caplog.set_level(logging.CRITICAL)
    with aioresponses() as mock, pytest.raises(Exception) as exc:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761592",
            payload={"blockHash": "a different hash"},
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761593",
            payload={"blockHash": "a different hash"},
        )
        check_orphan_blocks(ProtocolType.BITCOIN)

    block_bitcoin_761592_confirmed.refresh_from_db()
    block_bitcoin_761593_unconfirmed.refresh_from_db()
    assert block_bitcoin_761592_confirmed.is_orphan == False
    assert block_bitcoin_761593_unconfirmed.is_orphan == True
    assert isinstance(exc.value, Exception)
    assert str(exc.value) == "Critical: confirmed block is orphan"
    assert "Confirmed block 761592 is orphan for protocol 1" in caplog.text


@pytest.mark.usefixtures("db")
def test_confirm_blocks_nothing_new(
    block_bitcoin_761592_confirmed, block_bitcoin_761593_unconfirmed
):
    confirm_blocks(ProtocolType.BITCOIN, 761592)

    block_bitcoin_761592_confirmed.refresh_from_db()
    block_bitcoin_761593_unconfirmed.refresh_from_db()
    assert block_bitcoin_761592_confirmed.is_confirmed == True
    assert block_bitcoin_761593_unconfirmed.is_confirmed == False


@pytest.mark.usefixtures("db")
def test_confirm_blocks_new_block(
    mocker,
    block_bitcoin_761592_confirmed,
    block_bitcoin_761593_unconfirmed,
    block_bitcoin_761594_unconfirmed,
    block_bitcoin_761595_unconfirmed,
    transaction_single_bitcoin_address_one,
):
    mock_new_confirmed_transactions = mocker.patch(
        "transaction.tasks.new_confirmed_transactions.delay"
    )
    transaction_single_bitcoin_address_one.block_id = 761593
    transaction_single_bitcoin_address_one.is_confirmed = False
    transaction_single_bitcoin_address_one.save()

    confirm_blocks(ProtocolType.BITCOIN, 761594)

    block_bitcoin_761592_confirmed.refresh_from_db()
    block_bitcoin_761593_unconfirmed.refresh_from_db()
    block_bitcoin_761594_unconfirmed.refresh_from_db()
    block_bitcoin_761595_unconfirmed.refresh_from_db()
    assert block_bitcoin_761592_confirmed.is_confirmed == True
    assert block_bitcoin_761593_unconfirmed.is_confirmed == True
    assert block_bitcoin_761594_unconfirmed.is_confirmed == True
    assert block_bitcoin_761595_unconfirmed.is_confirmed == False
    transaction_single_bitcoin_address_one.refresh_from_db()
    assert transaction_single_bitcoin_address_one.is_confirmed == True
    mock_new_confirmed_transactions.assert_called_once_with(
        [transaction_single_bitcoin_address_one.id]
    )

    address_output = Address.objects.get(hash="17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k")
    assert Decimal(address_output.balance["BTC"]) == Decimal("0.00288733")
    address_input = Address.objects.get(
        hash="bc1qatd6clekcdlrjds3dzm64m3ukf9z2vfdz3hajy"
    )
    assert Decimal(address_input.balance["BTC"]) == Decimal("-0.00034930")
    assert Decimal(address_input.extended_public_key.balance["BTC"]) == Decimal(
        "-0.00034930"
    )


@pytest.mark.usefixtures("db", "rate_bitcoin_daily_four")
def test_digest_new_block(
    aioresponses,
    blockbook_block,
    single_bitcoin_address_three,
    single_bitcoin_address_four,
    single_bitcoin_address_five,
):
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/246469?page=1",
            payload=blockbook_block,
        )
        digest_new_block(ProtocolType.BITCOIN, 246468, 246469)

    blocks = Block.objects.all()
    assert blocks.count() == 1

    block = blocks.first()
    assert block.protocol_type == ProtocolType.BITCOIN
    assert block.block_id == 246469
    assert (
        block.block_hash
        == "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db"
    )
    assert block.is_confirmed == False
    assert block.is_orphan == False

    txs = Transaction.objects.all()
    assert txs.count() == 2

    tx_1 = txs[0]  # coinbase tx
    assert (
        tx_1.tx_id == "7c863e26ddd5f132485ff8637363ce9c3946b020b6ba563f3138511bae944e5b"
    )
    assert tx_1.protocol_type == ProtocolType.BITCOIN
    assert tx_1.block_id == 246469
    assert tx_1.block_time == datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc)
    assert tx_1.is_confirmed == True
    assert tx_1.details["fee"] == "0.0"
    assert tx_1.details["value_input"] == "0.0"
    assert tx_1.details["value_output"] == "25.1465"
    assert tx_1.details["asset_name"] == "BTC"
    assert (
        tx_1.details["block_hash"]
        == "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db"
    )
    assert tx_1.details["inputs"] == [
        {"address": None, "asset_name": "BTC", "amount_asset": "0.0"}
    ]
    assert tx_1.details["outputs"] == [
        {
            "address": "14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer",
            "asset_name": "BTC",
            "amount_asset": "25.1465",
        }
    ]
    assert tx_1.inputdata.all().count() == 0
    assert tx_1.outputdata.all().count() == 1
    tx_1_output = tx_1.outputdata.first()
    assert tx_1_output.address == single_bitcoin_address_three
    assert tx_1_output.amount_usd == "2403.502470"
    assert tx_1_output.amount_asset == "25.1465"
    assert tx_1_output.asset_name == "BTC"

    tx_2 = txs[1]
    assert (
        tx_2.tx_id == "de2d90d1042893f0a0775c86fb1e75b4095dce35a7ef70e5c10b2fb2db523920"
    )
    assert tx_2.protocol_type == ProtocolType.BITCOIN
    assert tx_2.block_id == 246469
    assert tx_2.block_time == datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc)
    assert tx_2.is_confirmed == True
    assert tx_2.details["fee"] == "0.0"
    assert tx_2.details["value_input"] == "313.14405178"
    assert tx_2.details["value_output"] == "313.14405178"
    assert tx_2.details["asset_name"] == "BTC"
    assert (
        tx_2.details["block_hash"]
        == "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db"
    )
    assert tx_2.details["inputs"] == [
        {
            "address": "1Dn274qviAhHXgq4e8Y5XmaBsnjhAB9GR8",
            "asset_name": "BTC",
            "amount_asset": "290.14405178",
        },
        {
            "address": "13HLjUPifi1uV9TwAatXGXhgJRg8Tee4EF",
            "asset_name": "BTC",
            "amount_asset": "23.0",
        },
    ]
    assert tx_2.details["outputs"] == [
        {
            "address": "1Fog84w3gEYkyDN6oaWaXbLuFqEF93uMho",
            "asset_name": "BTC",
            "amount_asset": "263.1904335",
        },
        {
            "address": "1EYNR7gGNqepznzjjDV1gsSSj53JopHnSA",
            "asset_name": "BTC",
            "amount_asset": "49.95361828",
        },
    ]
    assert tx_2.inputdata.all().count() == 1
    assert tx_2.outputdata.all().count() == 1
    tx_2_input = tx_2.inputdata.first()
    assert tx_2_input.address == single_bitcoin_address_four
    assert tx_2_input.amount_usd == "27731.9684691324"
    assert tx_2_input.amount_asset == "290.14405178"
    assert tx_2_input.asset_name == "BTC"
    tx_2_output = tx_2.outputdata.first()
    assert tx_2_output.address == single_bitcoin_address_five
    assert tx_2_output.amount_usd == "25155.741633930"
    assert tx_2_output.amount_asset == "263.1904335"
    assert tx_2_output.asset_name == "BTC"


@pytest.mark.usefixtures(
    "db",
    "single_bitcoin_address_three",
    "single_bitcoin_address_four",
    "single_bitcoin_address_five",
)
def test_digest_new_block_confirmed_block(aioresponses, blockbook_block):
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/246469?page=1",
            payload=blockbook_block,
        )
        digest_new_block(ProtocolType.BITCOIN, 246469, 246469)

    blocks = Block.objects.all()
    assert blocks.count() == 1
    block = blocks.first()
    assert block.is_confirmed == True


@pytest.mark.usefixtures(
    "db",
)
def test_digest_new_block_derive_new_addresses(
    aioresponses, blockbook_block, derived_bitcoin_address_three
):
    derived_bitcoin_address_three.hash = "14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer"
    derived_bitcoin_address_three.index = 0
    derived_bitcoin_address_three.save()

    assert (
        Address.objects.filter(
            extended_public_key=derived_bitcoin_address_three.extended_public_key
        ).count()
        == 1
    )

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/246469?page=1",
            payload=blockbook_block,
        )
        digest_new_block(ProtocolType.BITCOIN, 246469, 246469)

    blocks = Block.objects.all()
    assert blocks.count() == 1
    assert (
        Address.objects.filter(
            extended_public_key=derived_bitcoin_address_three.extended_public_key
        ).count()
        == 21
    )


@pytest.mark.usefixtures(
    "db",
    "single_bitcoin_address_three",
    "single_bitcoin_address_four",
    "single_bitcoin_address_five",
)
def test_sync_chain_of_blocks(
    aioresponses, blockbook_summary, blockbook_block_p1, blockbook_block_p2
):
    blockbook_summary["blockbook"]["bestHeight"] = 246469
    blocks = Block.objects.all()
    assert blocks.count() == 0
    assert Transaction.objects.all().count() == 0

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/246469?page=1",
            payload=blockbook_block_p1,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/246469?page=2",
            payload=blockbook_block_p2,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/", payload=blockbook_summary
        )
        sync_chain_of_blocks(ProtocolType.BITCOIN)

    assert blocks.count() == 1
    block = blocks.first()
    assert block.block_id == 246469
    assert Transaction.objects.all().count() == 2


@pytest.mark.usefixtures("db", "aioresponses", "block_bitcoin_761593_unconfirmed")
def test_sync_chain_of_blocks_with_block_id(mocker):
    mock_check_orphan_blocks = mocker.patch(
        "block.utils.check_orphan_blocks",
    )
    mock_digest_new_block = mocker.patch(
        "block.utils.digest_new_block",
    )
    mock_confirm_blocks = mocker.patch(
        "block.utils.confirm_blocks",
    )
    sync_chain_of_blocks(ProtocolType.BITCOIN, 761596)

    mock_check_orphan_blocks.assert_called_once()
    assert mock_digest_new_block.call_count == 3
    assert (
        repr(mock_digest_new_block.call_args_list[0])
        == "call(ProtocolType.BITCOIN, 761591, 761594)"
    )
    assert (
        repr(mock_digest_new_block.call_args_list[1])
        == "call(ProtocolType.BITCOIN, 761591, 761595)"
    )
    assert (
        repr(mock_digest_new_block.call_args_list[2])
        == "call(ProtocolType.BITCOIN, 761591, 761596)"
    )
    mock_confirm_blocks.assert_called_once_with(ProtocolType.BITCOIN, 761591)
