import pytest

from protocol import Protocol, ProtocolType


def test_current_block():
    bitcoin = Protocol(ProtocolType.BITCOIN)

    current_block = bitcoin.get_current_block()
    assert isinstance(current_block, int)


def test_xpub_details(hash_xpub_bitcoin_two):
    bitcoin = Protocol(ProtocolType.BITCOIN)

    xpub_content = bitcoin.backend.get_xpub(
        hash_xpub_bitcoin_two, details="txs", tokens="used"
    )
    assert isinstance(xpub_content["page"], int)
    assert isinstance(xpub_content["totalPages"], int)
    assert isinstance(xpub_content["txs"], int)
    assert xpub_content["address"] == hash_xpub_bitcoin_two
    assert isinstance(xpub_content["balance"], str)
    assert isinstance(xpub_content["transactions"], list)
    assert isinstance(xpub_content["tokens"], list)
    assert int(xpub_content["unconfirmedTxs"]) + int(xpub_content["txs"]) == len(
        xpub_content["transactions"]
    )

    transactions = xpub_content["transactions"]
    transaction = transactions[0]
    assert isinstance(transaction["txid"], str)
    assert isinstance(transaction["vin"], list)
    assert isinstance(transaction["vout"], list)
    assert isinstance(transaction["blockHash"], str)
    assert isinstance(transaction["blockHeight"], int)
    assert isinstance(transaction["confirmations"], int)
    assert isinstance(transaction["blockTime"], int)
    assert isinstance(transaction["value"], str)
    assert isinstance(transaction["valueIn"], str)
    assert isinstance(transaction["fees"], str)
    assert isinstance(transaction["hex"], str)

    vins = transaction["vin"]
    vin = vins[0]
    assert isinstance(vin["txid"], str)
    assert isinstance(vin["addresses"], list)
    assert isinstance(vin["value"], str)
    assert isinstance(vin["hex"], str)

    vouts = transaction["vout"]
    vout = vouts[0]
    assert isinstance(vout["addresses"], list)
    assert isinstance(vout["value"], str)
    assert isinstance(vout["hex"], str)


def test_address_details(hash_address_p2pkh_bitcoin_two):
    bitcoin = Protocol(ProtocolType.BITCOIN)

    address_content = bitcoin.backend.get_address(
        hash_address_p2pkh_bitcoin_two, details="txs"
    )
    assert isinstance(address_content["page"], int)
    assert isinstance(address_content["totalPages"], int)
    assert isinstance(address_content["txs"], int)
    assert address_content["address"] == hash_address_p2pkh_bitcoin_two
    assert isinstance(address_content["balance"], str)
    assert isinstance(address_content["transactions"], list)
    assert int(address_content["unconfirmedTxs"]) + int(address_content["txs"]) == len(
        address_content["transactions"]
    )

    transactions = address_content["transactions"]
    transaction = transactions[0]
    assert isinstance(transaction["txid"], str)
    assert isinstance(transaction["vin"], list)
    assert isinstance(transaction["vout"], list)
    assert isinstance(transaction["blockHash"], str)
    assert isinstance(transaction["blockHeight"], int)
    assert isinstance(transaction["confirmations"], int)
    assert isinstance(transaction["blockTime"], int)
    assert isinstance(transaction["value"], str)
    assert isinstance(transaction["valueIn"], str)
    assert isinstance(transaction["fees"], str)
    assert isinstance(transaction["hex"], str)

    vins = transaction["vin"]
    vin = vins[0]
    assert isinstance(vin["txid"], str)
    assert isinstance(vin["addresses"], list)
    assert isinstance(vin["value"], str)
    assert isinstance(vin["hex"], str)

    vouts = transaction["vout"]
    vout = vouts[0]
    assert isinstance(vout["addresses"], list)
    assert isinstance(vout["value"], str)
    assert isinstance(vout["hex"], str)


@pytest.mark.skip
def test_websocket(mocker):
    async def hashblock(self, block_hash):
        print(f"New block hash: {block_hash}")
        await self.sio.disconnect()

    mocker.patch(
        "protocol.bitcoin.websocket_blockbook.BlockBookSocketIOClient.hashblock",
        hashblock,
    )
    bitcoin = Protocol(ProtocolType.BITCOIN)
    bitcoin.wss_backend.start()
