import pytest

from protocol.bitcoin import BitcoinTestnet


def test_valid_xpublic_keys(valid_bitcoin_testnet_xpubs):
    for xpub in valid_bitcoin_testnet_xpubs:
        is_valid, semantic = BitcoinTestnet.validate_xpublic_key(xpub)
        assert is_valid == True
        assert semantic == "tpub"


def test_invalid_xpublic_keys(invalid_bitcoin_testnet_xpubs):
    for xpub in invalid_bitcoin_testnet_xpubs:
        is_valid, semantic = BitcoinTestnet.validate_xpublic_key(xpub)
        expected_semantic = "tpub" if xpub.startswith("tpub") else None
        assert is_valid == False
        assert semantic == expected_semantic


def test_valid_addresses(valid_bitcoin_testnet_addresses):
    semantics = ["P2PKH", "P2WPKH"]
    for index, address in enumerate(valid_bitcoin_testnet_addresses):
        expected_semantic_index = index % 2
        expected_semantic = semantics[expected_semantic_index]
        is_valid, semantic = BitcoinTestnet.validate_address(address)
        assert is_valid == True
        assert semantic == expected_semantic


def test_invalid_addresses(invalid_bitcoin_testnet_addresses):
    for address in invalid_bitcoin_testnet_addresses:
        is_valid, _ = BitcoinTestnet.validate_address(address)
        assert is_valid == False
