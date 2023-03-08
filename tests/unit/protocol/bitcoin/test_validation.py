import pytest  # noqa: F401

from protocol.bitcoin import Bitcoin


def test_valid_xpublic_keys(valid_bitcoin_xpubs):
    for xpub in valid_bitcoin_xpubs:
        is_valid, semantic = Bitcoin.validate_xpublic_key(xpub)
        assert is_valid is True
        assert semantic == "xpub"


def test_invalid_xpublic_keys(invalid_bitcoin_xpubs):
    for xpub in invalid_bitcoin_xpubs:
        is_valid, semantic = Bitcoin.validate_xpublic_key(xpub)
        expected_semantic = "xpub" if xpub.startswith("xpub") else None
        assert is_valid is False
        assert semantic == expected_semantic


def test_valid_addresses(valid_bitcoin_addresses):
    semantics = ["P2PKH", "P2WPKH"]
    for index, address in enumerate(valid_bitcoin_addresses):
        expected_semantic_index = index % 2
        expected_semantic = semantics[expected_semantic_index]
        is_valid, semantic = Bitcoin.validate_address(address)
        assert is_valid is True
        assert semantic == expected_semantic


def test_invalid_addresses(invalid_bitcoin_addresses):
    for address in invalid_bitcoin_addresses:
        is_valid, _ = Bitcoin.validate_address(address)
        assert is_valid is False
