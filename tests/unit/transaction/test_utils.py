import pytest
from datetime import datetime, timezone
from decimal import Decimal

from protocol.constants import ProtocolType
from protocol.bitcoin.backend_blockbook import BLOCKBOOK_SETTINGS
from transaction.models import Transaction
from transaction.utils import (
    sync_transactions_from_address,
    sync_transactions_from_extended_public_key,
)
from wallet.models import Address


@pytest.mark.usefixtures("db")
def test_sync_transactions_from_address(
    aioresponses,
    single_bitcoin_address_two,
    blockbook_address_details,
):
    queryset = Transaction.objects.all()
    assert queryset.count() == 0

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/address/{single_bitcoin_address_two.hash}?details=txs",
            payload=blockbook_address_details,
        )
        sync_transactions_from_address(single_bitcoin_address_two)

    assert queryset.count() == 4
    address_queryset = Address.objects.all()
    assert address_queryset.count() == 1
    tx_1 = queryset[0]
    assert (
        tx_1.tx_id == "b62aa5203fa27495ea431b91a5090aab741c8c39cc03ec4c1f4f4e157507595f"
    )
    assert tx_1.protocol_type == ProtocolType.BITCOIN
    assert tx_1.block_id == 509003
    assert tx_1.block_time == datetime(2018, 2, 13, 14, 29, tzinfo=timezone.utc)
    assert tx_1.is_confirmed == True
    assert tx_1.details["fee"] == "0.00002048"
    assert tx_1.details["value_input"] == "0.00067396"
    assert tx_1.details["value_output"] == "0.00065348"
    assert tx_1.details["asset_name"] == "BTC"
    assert (
        tx_1.details["block_hash"]
        == "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1"
    )
    assert tx_1.details["inputs"] == [
        {
            "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "asset_name": "BTC",
            "amount_asset": "0.00067396",
        }
    ]
    assert tx_1.details["outputs"] == [
        {
            "address": "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
            "asset_name": "BTC",
            "amount_asset": "0.00065348",
        }
    ]
    assert tx_1.inputdata.all().count() == 1
    tx_1_input = tx_1.inputdata.first()
    address = Address.objects.get(hash="1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8")
    assert address.extended_public_key == None
    assert address.protocol_type == ProtocolType.BITCOIN
    assert tx_1_input.address == address
    assert tx_1_input.amount_usd == None
    assert tx_1_input.amount_asset == "0.00067396"
    assert tx_1_input.asset_name == "BTC"
    tx_2 = queryset[1]
    assert (
        tx_2.tx_id == "a0a7e1bb6460bffed958bc80d74966be14fdec09608408de351053d1e8d653a1"
    )
    assert tx_2.protocol_type == ProtocolType.BITCOIN
    assert tx_2.block_id == 508998
    assert tx_2.block_time == datetime(2018, 2, 13, 13, 52, 16, tzinfo=timezone.utc)
    assert tx_2.is_confirmed == True
    assert tx_2.details["fee"] == "0.00065804"
    assert tx_2.details["value_input"] == "0.00560766"
    assert tx_2.details["value_output"] == "0.00494962"
    assert tx_2.details["asset_name"] == "BTC"
    assert (
        tx_2.details["block_hash"]
        == "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b"
    )
    assert tx_2.details["inputs"] == [
        {
            "address": "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
            "asset_name": "BTC",
            "amount_asset": "0.0003493",
        },
        {
            "address": "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
            "asset_name": "BTC",
            "amount_asset": "0.0023231",
        },
        {
            "address": "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
            "asset_name": "BTC",
            "amount_asset": "0.00293526",
        },
    ]
    assert tx_2.details["outputs"] == [
        {
            "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "asset_name": "BTC",
            "amount_asset": "0.00067396",
        },
        {
            "address": "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
            "asset_name": "BTC",
            "amount_asset": "0.00138833",
        },
        {
            "address": "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
            "asset_name": "BTC",
            "amount_asset": "0.00288733",
        },
    ]
    tx_2_output = tx_2.outputdata.first()
    assert tx_2_output.address == address
    assert tx_2_output.amount_usd == None
    assert tx_2_output.amount_asset == "0.00067396"
    assert tx_2_output.asset_name == "BTC"
    assert Decimal(address.balance["BTC"]) == Decimal("0")


@pytest.mark.usefixtures("db")
def test_sync_transactions_from_extended_public_key(
    aioresponses,
    xpublic_key_bitcoin_two,
    blockbook_xpub_details,
    blockbook_xpub_details_p2wpkh,
):
    queryset = Transaction.objects.all()
    assert queryset.count() == 0

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/pkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/wpkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details_p2wpkh,
        )
        sync_transactions_from_extended_public_key(xpublic_key_bitcoin_two)

    assert queryset.count() == 16
    address_queryset = Address.objects.all()
    assert address_queryset.count() == 45
    tx_1 = queryset[0]
    assert (
        tx_1.tx_id == "b62aa5203fa27495ea431b91a5090aab741c8c39cc03ec4c1f4f4e157507595f"
    )
    assert tx_1.protocol_type == ProtocolType.BITCOIN
    assert tx_1.block_id == 509003
    assert tx_1.block_time == datetime(2018, 2, 13, 14, 29, tzinfo=timezone.utc)
    assert tx_1.is_confirmed == True
    assert tx_1.details["fee"] == "0.00002048"
    assert tx_1.details["value_input"] == "0.00067396"
    assert tx_1.details["value_output"] == "0.00065348"
    assert tx_1.details["asset_name"] == "BTC"
    assert (
        tx_1.details["block_hash"]
        == "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1"
    )
    assert tx_1.inputdata.all().count() == 1
    tx_1_input = tx_1.inputdata.first()
    address = Address.objects.get(hash="1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8")
    assert address.extended_public_key == xpublic_key_bitcoin_two
    assert address.protocol_type == ProtocolType.BITCOIN
    assert address.is_change == False
    assert address.index == 24
    assert address.details["semantic"] == "P2PKH"
    assert tx_1_input.address == address
    assert tx_1_input.amount_usd == None
    assert tx_1_input.amount_asset == "0.00067396"
    assert tx_1_input.asset_name == "BTC"
    tx_2 = queryset[1]
    assert (
        tx_2.tx_id == "a0a7e1bb6460bffed958bc80d74966be14fdec09608408de351053d1e8d653a1"
    )
    assert tx_2.protocol_type == ProtocolType.BITCOIN
    assert tx_2.block_id == 508998
    assert tx_2.block_time == datetime(2018, 2, 13, 13, 52, 16, tzinfo=timezone.utc)
    assert tx_2.is_confirmed == True
    assert tx_2.details["fee"] == "0.00065804"
    assert tx_2.details["value_input"] == "0.00560766"
    assert tx_2.details["value_output"] == "0.00494962"
    assert tx_2.details["asset_name"] == "BTC"
    assert (
        tx_2.details["block_hash"]
        == "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b"
    )
    tx_2_output = tx_2.outputdata.first()
    assert tx_2_output.address == address
    assert tx_2_output.amount_usd == None
    assert tx_2_output.amount_asset == "0.00067396"
    assert tx_2_output.asset_name == "BTC"
    assert Decimal(address.balance["BTC"]) == Decimal("0")
    xpublic_key_bitcoin_two.refresh_from_db()
    assert Decimal(xpublic_key_bitcoin_two.balance["BTC"]) == Decimal("0")


@pytest.mark.usefixtures("db")
def test_sync_transactions_from_extended_public_key_partial_response(
    aioresponses,
    xpublic_key_bitcoin_two,
    blockbook_xpub_details,
    blockbook_xpub_details_p2wpkh,
):
    queryset = Transaction.objects.all()
    assert queryset.count() == 0

    blockbook_xpub_details["transactions"] = blockbook_xpub_details["transactions"][:7]

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/pkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/wpkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details_p2wpkh,
        )
        sync_transactions_from_extended_public_key(xpublic_key_bitcoin_two)

    assert queryset.count() == 7
    xpublic_key_bitcoin_two.refresh_from_db()
    assert Decimal(xpublic_key_bitcoin_two.balance["BTC"]) == Decimal("-0.00050000")
    address = Address.objects.get(hash="12CL4K2eVqj7hQTix7dM7CVHCkpP17Pry3")
    assert Decimal(address.balance["BTC"]) == Decimal("-0.00050000")


@pytest.mark.usefixtures("db")
def test_sync_transactions_from_extended_public_key_partial_response_unconfirmed(
    aioresponses,
    xpublic_key_bitcoin_two,
    blockbook_xpub_details,
    blockbook_xpub_details_p2wpkh,
):
    queryset = Transaction.objects.all()
    assert queryset.count() == 0

    blockbook_xpub_details["transactions"] = blockbook_xpub_details["transactions"][:7]
    for transaction in blockbook_xpub_details["transactions"]:
        transaction["confirmations"] = 0

    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/pkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/wpkh({xpublic_key_bitcoin_two.hash})?details=txs&tokens=used",
            payload=blockbook_xpub_details_p2wpkh,
        )
        sync_transactions_from_extended_public_key(xpublic_key_bitcoin_two)

    assert queryset.count() == 7
    xpublic_key_bitcoin_two.refresh_from_db()
    assert "BTC" not in xpublic_key_bitcoin_two.balance
    address = Address.objects.get(hash="12CL4K2eVqj7hQTix7dM7CVHCkpP17Pry3")
    assert "BTC" not in address.balance
