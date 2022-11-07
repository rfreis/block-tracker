import pytest
from datetime import datetime, timezone
from decimal import Decimal

from tests.fixtures.utils import json_from_file


@pytest.fixture
def hash_xpub_bitcoin_one():
    return "xpub6FECBnuFWCiEEGJQWcKUgRqQ7ecZNNz1xpxWVLgyA7kcHPjdJhFLnJZbQbvQSPVr2R9xVWXjoVgGUom21dw9AkQkiKKz2YYGYGUdj7RaiNA"


@pytest.fixture
def hash_xpub_bitcoin_two():
    return "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"


@pytest.fixture
def hash_tx_xpub_bitcoin_two():
    return "36b92e05aa5aeb4ca09393185b49a558cdad8870c0e0e53b3e041d95628a9761"


@pytest.fixture
def block_height_and_hash_tx_xpub_bitcoin_two():
    return 246469, "00000000000000836597cc216daeda1e7d82361a04312f29bf75c12b511bb2db"


@pytest.fixture
def hash_address_p2pkh_bitcoin_one():
    return "1NQpH6Nf8QtR2HphLRcvuVqfhXBXsiWn8r"


@pytest.fixture
def hash_address_p2pkh_bitcoin_two():
    return "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8"


@pytest.fixture
def hash_address_p2pkh_bitcoin_three():
    return "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k"


@pytest.fixture
def hash_address_p2wpkh_bitcoin_one():
    return "bc1qatd6clekcdlrjds3dzm64m3ukf9z2vfdz3hajy"


@pytest.fixture
def hash_address_p2wpkh_bitcoin_two():
    return "bc1qgqpdyqtgwx9vhsasth59qjcn33apxsmdv3sgw7"


@pytest.fixture
def valid_bitcoin_xpubs():
    return [
        "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",
    ]


@pytest.fixture
def invalid_bitcoin_xpubs():
    return [
        "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMCet8",
        "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvggDnw",
        "xpub661MyMwAqRbcEYS8w7XLSVeEsBXy79zSzH1J8vCdxAZningWLdN3zgtU6Txnt3siSujt9RCVYsx4qHZGc62TG4McvMGcAUjeuwZdduYEvFn",
        "xpub661MyMwAqRbcEYS8w7XLSVeEsBXy79zSzH1J8vCdxAZningWLdN3zgtU6N8ZMMXctdiCjxTNq964yKkwrkBJJwpzZS4HS2fxvyYUA4q2Xe4",
        "xpub661no6RGEX3uJkY4bNnPcw4URcQTrSibUZ4NqJEw5eBkv7ovTwgiT91XX27VbEXGENhYRCf7hyEbWrR3FewATdCEebj6znwMfQkhRYHRLpJ",
        "xpub661MyMwAuDcm6CRQ5N4qiHKrJ39Xe1R1NyfouMKTTWcguwVcfrZJaNvhpebzGerh7gucBvzEQWRugZDuDXjNDRmXzSZe4c7mnTK97pTvGS8",
        "DMwo58pR1QLEFihHiXPVykYB6fJmsTeHvyTp7hRThAtCX8CvYzgPcn8XnmdfHGMQzT7ayAmfo4z3gY5KfbrZWZ6St24UVf2Qgo6oujFktLHdHY4",
        "xpub661MyMwAqRbcEYS8w7XLSVeEsBXy79zSzH1J8vCdxAZningWLdN3zgtU6Q5JXayek4PRsn35jii4veMimro1xefsM58PgBMrvdYre8QyULY",
    ]


@pytest.fixture
def valid_bitcoin_addresses():
    return [
        "1NQpH6Nf8QtR2HphLRcvuVqfhXBXsiWn8r",
        "bc1qatd6clekcdlrjds3dzm64m3ukf9z2vfdz3hajy",
        "1DK5Do88Vi2p7mbCcSsrug3wGH99G8LNY1",
        "bc1qsuxg2xz7x5zlg5ygweassgefk7gk9q50y2m3zq",
        "17KnnPrAjHi1ZJaPRa9nkwXCy5nkwB6kRF",
        "bc1qg408t8nlvse9fhfmhnug27xg85aw6cg9s3wrcu",
    ]


@pytest.fixture
def invalid_bitcoin_addresses():
    return [
        "1NQpH6Nf8QtR2HphLRcvuVqfhXBXsiWN8r",
        "bc1qatd6clekcdlrjds3dzm64m3ukf9z2vfdz3hzjy",
        "1DK5Do88Vi2p7mbCcSsrug3wGH99G8LnY1",
        "bc1qsuxg2xz7x5zlg5ygweassgefk7gk9q50y2m2zq",
        "17KnnPrAjHi1ZJaPRa9nkwXCy5nkwB6KRF",
        "bc1qg408t8nlvse9fhfmhnug27xg85aw6cg9s3wzcu",
        "7KnnPrAjHi1ZJaPRa9nkwXCy5nkwB6KRF",
    ]


@pytest.fixture
def ckd_bitcoin_hashes():
    content = json_from_file("tests/fixtures/protocol/data/bitcoin_ckd.json")
    return content


@pytest.fixture
def blockbook_summary():
    content = json_from_file(
        "tests/fixtures/protocol/data/bitcoin_blockbook_summary.json"
    )
    return content


@pytest.fixture
def blockbook_xpub_details():
    content = json_from_file("tests/fixtures/protocol/data/bitcoin_blockbook_xpub.json")
    return content


@pytest.fixture
def blockbook_xpub_details_p2wpkh():
    content = json_from_file(
        "tests/fixtures/protocol/data/bitcoin_blockbook_xpub_p2wpkh.json"
    )
    return content
