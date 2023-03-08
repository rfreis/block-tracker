import pytest  # noqa: F401

from tests.fixtures.utils import json_from_file


@pytest.fixture
def current_bitcoin_price():
    return {"bitcoin": {"usd": 17902.133058411408}}


@pytest.fixture
def daily_bitcoin_history():
    content = json_from_file(
        "tests/fixtures/rate/data/coingecko_daily_bitcoin_history.json"
    )
    return content
