import pytest  # noqa: F401

from protocol.bitcoin import BitcoinTestnet

from .test_ckd import _validate_ckd


def test_ckd_format(ckd_bitcoin_testnet_hashes):
    xpub = ckd_bitcoin_testnet_hashes["xpub"]
    data = BitcoinTestnet.derive_addresses_from_xpublic_key(xpub, end=0)
    expected_data = [
        {
            "index": 0,
            "address": "n2vma9TdwSKfoQJK3zbJjR3zZWnEsxiEYt",
            "semantic": "P2PKH",
            "is_change": False,
        },
        {
            "index": 0,
            "address": "tb1qatd6clekcdlrjds3dzm64m3ukf9z2vfdghvwfh",
            "semantic": "P2WPKH",
            "is_change": False,
        },
        {
            "index": 0,
            "address": "mtqqrAJambsRtPeg2TY5bb1w1VjTmuSbhu",
            "semantic": "P2PKH",
            "is_change": True,
        },
        {
            "index": 0,
            "address": "tb1qjgkzss0j03rh37tm5mr3uznedpdx7tzqsazega",
            "semantic": "P2WPKH",
            "is_change": True,
        },
    ]
    assert data == expected_data


def test_ckd(ckd_bitcoin_testnet_hashes):
    xpub = ckd_bitcoin_testnet_hashes["xpub"]
    ckd_addresses = [
        *BitcoinTestnet.derive_addresses_from_xpublic_key(xpub, end=49),
        *BitcoinTestnet.derive_addresses_from_xpublic_key(
            xpub, start=1000000000, end=1000000000
        ),
        *BitcoinTestnet.derive_addresses_from_xpublic_key(
            xpub, start=2147483647, end=2147483647
        ),
    ]
    _validate_ckd(ckd_bitcoin_testnet_hashes, ckd_addresses)
