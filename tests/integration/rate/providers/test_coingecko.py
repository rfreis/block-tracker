import pytest  # noqa: F401

from rate.provider.coingecko import CoinGeckoProvider


@pytest.mark.asyncio
async def test_get_history():
    provider = CoinGeckoProvider()
    content = await provider._get_daily_history("bitcoin")

    assert "prices" in content
    assert isinstance(content["prices"], list)


@pytest.mark.asyncio
async def test_current_price():
    provider = CoinGeckoProvider()
    content = await provider._get_current_price("bitcoin")

    assert "bitcoin" in content
    assert "usd" in content["bitcoin"]
    assert isinstance(content["bitcoin"]["usd"], float)
