from datetime import datetime, timezone

import pytest  # noqa: F401
from freezegun import freeze_time

from rate.constants import RateInterval
from rate.provider.coingecko import CoinGeckoProvider


@pytest.mark.asyncio
async def test_get_daily_history(aioresponses, daily_bitcoin_history):
    with aioresponses() as mock:
        mock.get(
            f"{CoinGeckoProvider.BASE_URL}/coins/bitcoin/market_chart?vs_currency=usd&days=max&interval=daily",
            payload=daily_bitcoin_history,
        )
        provider = CoinGeckoProvider()
        content = await provider.get_daily_history("BTC")

    assert len(content) == 3516
    assert content[0] == {
        "time": datetime(2013, 4, 28, 0, 0, tzinfo=timezone.utc),
        "asset_name": "BTC",
        "interval": RateInterval.DAILY,
        "amount_usd": "135.3",
    }


@freeze_time("2022-12-13 15:36:50")
@pytest.mark.usefixtures("db")
@pytest.mark.asyncio
async def test_get_daily_history_with_history(
    aioresponses, daily_bitcoin_history, rate_bitcoin_daily_one
):
    with aioresponses() as mock:
        mock.get(
            f"{CoinGeckoProvider.BASE_URL}/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=daily",
            payload=daily_bitcoin_history,
        )
        provider = CoinGeckoProvider()
        content = await provider.get_daily_history("BTC", rate_bitcoin_daily_one.time)

    assert len(content) == 3516
    assert content[0] == {
        "time": datetime(2013, 4, 28, 0, 0, tzinfo=timezone.utc),
        "asset_name": "BTC",
        "interval": RateInterval.DAILY,
        "amount_usd": "135.3",
    }


@freeze_time("2022-12-13 15:36:50")
@pytest.mark.usefixtures("db")
@pytest.mark.asyncio
async def test_get_daily_history_with_history_today(
    aioresponses, rate_bitcoin_daily_two
):
    with aioresponses():
        provider = CoinGeckoProvider()
        content = await provider.get_daily_history("BTC", rate_bitcoin_daily_two.time)

    assert content == []


@freeze_time("2022-12-13 15:36:50")
@pytest.mark.asyncio
async def test_get_current_price(aioresponses, current_bitcoin_price):
    with aioresponses() as mock:
        mock.get(
            f"{CoinGeckoProvider.BASE_URL}/simple/price?ids=bitcoin&vs_currencies=usd&precision=full",
            payload=current_bitcoin_price,
        )
        provider = CoinGeckoProvider()
        content = await provider.get_current_price("BTC")

    assert content == {
        "time": datetime(2022, 12, 13, 15, 36, 50, tzinfo=timezone.utc),
        "asset_name": "BTC",
        "interval": RateInterval.FIVE_MIN,
        "amount_usd": "17902.133058411408",
    }
