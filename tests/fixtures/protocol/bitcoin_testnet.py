import pytest  # noqa: F401

from tests.fixtures.utils import json_from_file


@pytest.fixture
def hash_xpub_bitcoin_testnet_one():
    return "tpubDCas76a7WztxfXEdVsY4tCH48PiMwwB7DjAARt5vWxvzgvUT4qMHTkxC9Bch4WEDLtDLHS1XJhZDSyW4UpK7rAZwfvHFuveTYuiBxKAEB51"


@pytest.fixture
def hash_address_p2pkh_bitcoin_testnet_one():
    return "n2vma9TdwSKfoQJK3zbJjR3zZWnEsxiEYt"


@pytest.fixture
def hash_address_p2wpkh_bitcoin_testnet_one():
    return "tb1qatd6clekcdlrjds3dzm64m3ukf9z2vfdghvwfh"


@pytest.fixture
def valid_bitcoin_testnet_xpubs():
    return [
        "tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp",
        "tpubDCas76a7WztxfXEdVsY4tCH48PiMwwB7DjAARt5vWxvzgvUT4qMHTkxC9Bch4WEDLtDLHS1XJhZDSyW4UpK7rAZwfvHFuveTYuiBxKAEB51",
        "tpubDHX88eY7FGhdgrcHW5TBdMrxTvzvQhuuZHbftDWs87RMiCuR3u3oSW83aL4oAUMLQw2tjx9zBkpoYgDYyFeGSoKfo6dZdTf6zUndF9Szgf9",
    ]


@pytest.fixture
def invalid_bitcoin_testnet_xpubs():
    return [
        "tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhWo4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87Vkp",
        "tpubDCas76a7WztxfXEdVsY4tCH48PiMwwB7DjAARt5vWxvzgvUT4qMHTkxC9Bch4WEDLtDLHS1XJhZDSyW4UpK7rAZwfvHFuveTYuiBxKAEB41",
        "tpubDHX88eY7FGhdgrcHW5TBdMrxTvzvQhuuZHbftDWs87RMiCuR3u3oSW83aL4oAUMLQw2tjx9zBkpoYgDYyFeGSoKfo6dZdTf6zUndF9SzgF9",
    ]


@pytest.fixture
def valid_bitcoin_testnet_addresses():
    return [
        "n2vma9TdwSKfoQJK3zbJjR3zZWnEsxiEYt",
        "tb1qatd6clekcdlrjds3dzm64m3ukf9z2vfdghvwfh",
        "my7Cjy9EbKYEXHEmsvRFVWDSpNp8tSEqUd",
    ]


@pytest.fixture
def invalid_bitcoin_testnet_addresses():
    return [
        "n2vma9TdwSKfoQJK3zbJjR3zZWnEsxiEyt",
        "tb1qatd6clekcdlrjds3dzm64m3ukf9z2vfdghvweh",
        "my7Cjy9EbKYEXHEmsvRFVWDSpNp8tSEqud",
    ]


@pytest.fixture
def ckd_bitcoin_testnet_hashes():
    content = json_from_file("tests/fixtures/protocol/data/bitcoin_testnet_ckd.json")
    return content


@pytest.fixture
def bitcoin_testnet_block_with_empty_address():
    content = json_from_file(
        "tests/fixtures/protocol/data/bitcoin_testnet_block_2422855.json"
    )
    return content
