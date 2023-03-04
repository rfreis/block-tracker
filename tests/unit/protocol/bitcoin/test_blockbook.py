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


def test_block_hash(aioresponses, block_hashes_by_id):
    bitcoin = Bitcoin()
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block-index/761592",
            payload={"blockHash": block_hashes_by_id[761592]},
        )
        block_hash = bitcoin.get_block_hash(761592)

    assert (
        block_hash == "00000000000000000003a742d44aec4caf50c3889646e9e7936057b892485ec7"
    )


def test_get_block(aioresponses, blockbook_block_p1, blockbook_block_p2):
    bitcoin = Bitcoin(ProtocolType.BITCOIN)
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/761592?page=1",
            payload=blockbook_block_p1,
        )
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/761592?page=2",
            payload=blockbook_block_p2,
        )
        content = bitcoin.get_block(761592)

    expected_content = {
        "block_id": 761592,
        "block_hash": "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db",
        "txs": [
            {
                "protocol_type": ProtocolType.BITCOIN,
                "tx_id": "7c863e26ddd5f132485ff8637363ce9c3946b020b6ba563f3138511bae944e5b",
                "block_id": 246469,
                "block_time": datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc),
                "is_confirmed": True,
                "details": {
                    "value_input": "0.0",
                    "value_output": "25.1465",
                    "fee": "0.0",
                    "asset_name": "BTC",
                    "block_hash": "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db",
                },
                "addresses": ["14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer"],
                "inputs": [
                    {
                        "amount_asset": Decimal("0.0"),
                        "asset_name": "BTC",
                        "address": None,
                    }
                ],
                "outputs": [
                    {
                        "amount_asset": Decimal("25.1465"),
                        "asset_name": "BTC",
                        "address": "14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer",
                    }
                ],
            },
            {
                "protocol_type": ProtocolType.BITCOIN,
                "tx_id": "de2d90d1042893f0a0775c86fb1e75b4095dce35a7ef70e5c10b2fb2db523920",
                "block_id": 246469,
                "block_time": datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc),
                "is_confirmed": True,
                "details": {
                    "value_input": "313.14405178",
                    "value_output": "313.14405178",
                    "fee": "0.0",
                    "asset_name": "BTC",
                    "block_hash": "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db",
                },
                "addresses": [
                    "1Dn274qviAhHXgq4e8Y5XmaBsnjhAB9GR8",
                    "13HLjUPifi1uV9TwAatXGXhgJRg8Tee4EF",
                    "1Fog84w3gEYkyDN6oaWaXbLuFqEF93uMho",
                    "1EYNR7gGNqepznzjjDV1gsSSj53JopHnSA",
                ],
                "inputs": [
                    {
                        "amount_asset": Decimal("290.14405178"),
                        "asset_name": "BTC",
                        "address": "1Dn274qviAhHXgq4e8Y5XmaBsnjhAB9GR8",
                    },
                    {
                        "amount_asset": Decimal("23.0"),
                        "asset_name": "BTC",
                        "address": "13HLjUPifi1uV9TwAatXGXhgJRg8Tee4EF",
                    },
                ],
                "outputs": [
                    {
                        "amount_asset": Decimal("263.1904335"),
                        "asset_name": "BTC",
                        "address": "1Fog84w3gEYkyDN6oaWaXbLuFqEF93uMho",
                    },
                    {
                        "amount_asset": Decimal("49.95361828"),
                        "asset_name": "BTC",
                        "address": "1EYNR7gGNqepznzjjDV1gsSSj53JopHnSA",
                    },
                ],
            },
            {
                "protocol_type": ProtocolType.BITCOIN,
                "tx_id": "fc50c33bc63cbf2e07283377702e265662f1040b717d4fbdb89659c2c24c89d3",
                "block_id": 246469,
                "block_time": datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc),
                "is_confirmed": True,
                "details": {
                    "value_input": "5.0",
                    "value_output": "5.0",
                    "fee": "0.0",
                    "asset_name": "BTC",
                    "block_hash": "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db",
                },
                "addresses": [
                    "1CzAncjXYjtiXNC4CNAw4RoKdQLoi72xn",
                    "189Zh94AW7E53y2YGEeDyDUnDiN34XZLdh",
                    "1CzAncjXYjtiXNC4CNAw4RoKdQLoi72xn",
                ],
                "inputs": [
                    {
                        "amount_asset": Decimal("5.0"),
                        "asset_name": "BTC",
                        "address": "1CzAncjXYjtiXNC4CNAw4RoKdQLoi72xn",
                    }
                ],
                "outputs": [
                    {
                        "amount_asset": Decimal("1.0"),
                        "asset_name": "BTC",
                        "address": "189Zh94AW7E53y2YGEeDyDUnDiN34XZLdh",
                    },
                    {
                        "amount_asset": Decimal("4.0"),
                        "asset_name": "BTC",
                        "address": "1CzAncjXYjtiXNC4CNAw4RoKdQLoi72xn",
                    },
                ],
            },
            {
                "protocol_type": ProtocolType.BITCOIN,
                "tx_id": "4fb0a91e435e4aac62c1a82f68ea9fb607e86075ce9dc15c019b4139a45e0d0f",
                "block_id": 246469,
                "block_time": datetime(2013, 7, 14, 4, 0, 52, tzinfo=timezone.utc),
                "is_confirmed": True,
                "details": {
                    "value_input": "101.93498796",
                    "value_output": "101.93448796",
                    "fee": "0.0005",
                    "asset_name": "BTC",
                    "block_hash": "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db",
                },
                "addresses": [
                    "11G9xXi3SWpFu6GBZWobh47Nas4X4JGjy",
                    "1DGu3AkG8ATKEL1GFNxztwqrdBZhVZRKf6",
                    "1HJgmjxSg7v31uZvyLfPx3txim2QK6zNYi",
                ],
                "inputs": [
                    {
                        "amount_asset": Decimal("101.93498796"),
                        "asset_name": "BTC",
                        "address": "11G9xXi3SWpFu6GBZWobh47Nas4X4JGjy",
                    }
                ],
                "outputs": [
                    {
                        "amount_asset": Decimal("101.93328796"),
                        "asset_name": "BTC",
                        "address": "1DGu3AkG8ATKEL1GFNxztwqrdBZhVZRKf6",
                    },
                    {
                        "amount_asset": Decimal("0.0012"),
                        "asset_name": "BTC",
                        "address": "1HJgmjxSg7v31uZvyLfPx3txim2QK6zNYi",
                    },
                ],
            },
        ],
    }

    assert content == expected_content


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
            "asset_name": "BTC",
            "block_hash": "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1",
        },
        "addresses": [
            "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
        ],
        "inputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            }
        ],
        "outputs": [
            {
                "amount_asset": Decimal("0.00065348"),
                "asset_name": "BTC",
                "address": "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
            }
        ],
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
            "asset_name": "BTC",
            "block_hash": "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b",
        },
        "addresses": [
            "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
            "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
            "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
            "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
            "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
        ],
        "inputs": [
            {
                "amount_asset": Decimal("0.0003493"),
                "asset_name": "BTC",
                "address": "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
            },
            {
                "amount_asset": Decimal("0.0023231"),
                "asset_name": "BTC",
                "address": "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
            },
            {
                "amount_asset": Decimal("0.00293526"),
                "asset_name": "BTC",
                "address": "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
            },
        ],
        "outputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            },
            {
                "amount_asset": Decimal("0.00138833"),
                "asset_name": "BTC",
                "address": "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
            },
            {
                "amount_asset": Decimal("0.00288733"),
                "asset_name": "BTC",
                "address": "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
            },
        ],
    }
    assert content["last_used_indexes"] == {"P2PKH": {"receive": 24, "change": 0}}


def test_get_transactions_from_address(
    aioresponses,
    hash_address_p2pkh_bitcoin_two,
    blockbook_address_details,
):
    bitcoin = Bitcoin(ProtocolType.BITCOIN)
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/address/{hash_address_p2pkh_bitcoin_two}?details=txs",
            payload=blockbook_address_details,
        )
        transactions = bitcoin.get_transactions_from_address(
            hash_address_p2pkh_bitcoin_two
        )

    assert len(transactions) == 4
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
            "asset_name": "BTC",
            "block_hash": "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1",
        },
        "addresses": [
            "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
        ],
        "inputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            }
        ],
        "outputs": [
            {
                "amount_asset": Decimal("0.00065348"),
                "asset_name": "BTC",
                "address": "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
            }
        ],
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
            "asset_name": "BTC",
            "block_hash": "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b",
        },
        "addresses": [
            "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
            "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
            "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
            "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
            "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
        ],
        "inputs": [
            {
                "amount_asset": Decimal("0.0003493"),
                "asset_name": "BTC",
                "address": "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
            },
            {
                "amount_asset": Decimal("0.0023231"),
                "asset_name": "BTC",
                "address": "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
            },
            {
                "amount_asset": Decimal("0.00293526"),
                "asset_name": "BTC",
                "address": "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
            },
        ],
        "outputs": [
            {
                "amount_asset": Decimal("0.00067396"),
                "asset_name": "BTC",
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
            },
            {
                "amount_asset": Decimal("0.00138833"),
                "asset_name": "BTC",
                "address": "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
            },
            {
                "amount_asset": Decimal("0.00288733"),
                "asset_name": "BTC",
                "address": "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
            },
        ],
    }


@pytest.mark.asyncio
async def test_wss_backend(mocker, block_height_and_hash_tx_xpub_bitcoin_two):
    mock_new_block = mocker.patch(
        "protocol.utils.blockbook.celery_app.send_task",
    )
    _, block_hash = block_height_and_hash_tx_xpub_bitcoin_two

    bitcoin = Bitcoin(ProtocolType.BITCOIN)
    await bitcoin.wss_backend.hashblock(block_hash)

    mock_new_block.assert_called_once_with(
        "block.tasks.new_block_hash", (ProtocolType.BITCOIN, block_hash)
    )


def test_get_block_with_empty_address(
    aioresponses, bitcoin_testnet_block_with_empty_address
):
    bitcoin = Bitcoin(ProtocolType.BITCOIN)
    with aioresponses() as mock:
        mock.get(
            f"{BLOCKBOOK_SETTINGS['Bitcoin']['url']}/api/v2/block/2422855?page=1",
            payload=bitcoin_testnet_block_with_empty_address,
        )
        content = bitcoin.get_block(2422855)

    assert len(content["txs"]) == 1
    assert len(content["txs"][0]["addresses"]) == 1
