import pytest
from datetime import datetime, timezone
from freezegun import freeze_time

from rate.constants import RateInterval
from rate.models import Rate
from rate.provider.coingecko import CoinGeckoProvider
from rate.utils import sync_rates


@freeze_time("2022-12-13 15:36:50")
@pytest.mark.usefixtures("db")
def test_sync_rates(aioresponses, daily_bitcoin_history, current_bitcoin_price):
    with aioresponses() as mock:
        mock.get(
            f"{CoinGeckoProvider.BASE_URL}/coins/bitcoin/market_chart?vs_currency=usd&days=max&interval=daily",
            payload=daily_bitcoin_history,
        )
        mock.get(
            f"{CoinGeckoProvider.BASE_URL}/simple/price?ids=bitcoin&vs_currencies=usd&precision=full",
            payload=current_bitcoin_price,
        )
        sync_rates()

    assert Rate.objects.all().count() == 3517

    daily_one = Rate.objects.filter(interval=RateInterval.DAILY).first()
    assert daily_one.asset_name == "BTC"
    assert daily_one.amount_usd == "135.3"
    assert daily_one.time == datetime(2013, 4, 28, 0, 0, tzinfo=timezone.utc)

    current_one = Rate.objects.filter(interval=RateInterval.FIVE_MIN).first()
    assert current_one.asset_name == "BTC"
    assert current_one.amount_usd == "17902.133058411408"
    assert current_one.time == datetime(2022, 12, 13, 15, 36, 50, tzinfo=timezone.utc)
