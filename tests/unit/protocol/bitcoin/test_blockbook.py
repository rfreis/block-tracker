import pytest
from datetime import datetime, timezone
from decimal import Decimal

from protocol.bitcoin import Bitcoin
from protocol.bitcoin.backend_blockbook import BLOCKBOOK_SETTINGS
from protocol.constants import ProtocolType


def test_current_block(aioresponses, blockbook_summary):
    bitcoin = Bitcoin()
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/", payload=blockbook_summary
        )
        current_block = bitcoin.get_current_block()

    assert current_block == 761598


def test_get_transactions_from_xpublic_key(
    aioresponses,
    hash_xpub_bitcoin_two,
    blockbook_xpub_details,
    blockbook_xpub_details_p2wpkh,
):
    bitcoin = Bitcoin(ProtocolType.BITCOIN)
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/pkh({hash_xpub_bitcoin_two})?details=txs&tokens=used",
            payload=blockbook_xpub_details,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/xpub/wpkh({hash_xpub_bitcoin_two})?details=txs&tokens=used",
            payload=blockbook_xpub_details_p2wpkh,
        )
        content = bitcoin.get_transactions_from_xpublic_key(hash_xpub_bitcoin_two)

    transactions = content["txs"]
    assert len(transactions) == 16
    assert transactions[0] == {
        "protocol_type": ProtocolType.BITCOIN,
        "tx_id": "b62aa5203fa27495ea431b91a5090aab741c8c39cc03ec4c1f4f4e157507595f",
        "block_id": 509003,
        "block_time": datetime(2018, 2, 13, 14, 29, tzinfo=timezone.utc),
        "is_confirmed": True,
        "details": {
            "value_input": "0.00067396",
            "value_output": "0.00065348",
            "fee": "0.00002048",
            "block_hash": "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1",
        },
        "inputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            }
        ],
        "outputs": [],
    }
    assert transactions[1] == {
        "protocol_type": ProtocolType.BITCOIN,
        "tx_id": "a0a7e1bb6460bffed958bc80d74966be14fdec09608408de351053d1e8d653a1",
        "block_id": 508998,
        "block_time": datetime(2018, 2, 13, 13, 52, 16, tzinfo=timezone.utc),
        "is_confirmed": True,
        "details": {
            "value_input": "0.00560766",
            "value_output": "0.00494962",
            "fee": "0.00065804",
            "block_hash": "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b",
        },
        "inputs": [],
        "outputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            }
        ],
    }
    assert content["last_used_indexes"] == {"P2PKH": {"receive": 24, "change": 0}}
