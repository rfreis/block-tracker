import pytest
from datetime import datetime, timezone

from rate.constants import RateInterval
from rate.models import Rate


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_daily_one():
    rate = Rate.objects.create(
        time=datetime(2022, 12, 12, 0, 0, tzinfo=timezone.utc),
        asset_name="BTC",
        interval=RateInterval.DAILY,
        amount_usd="17101.038019732932",
    )
    yield rate
    rate.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_daily_two():
    rate = Rate.objects.create(
        time=datetime(2022, 12, 13, 0, 0, tzinfo=timezone.utc),
        asset_name="BTC",
        interval=RateInterval.DAILY,
        amount_usd="17179.596038203494",
    )
    yield rate
    rate.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_daily_three():
    rate = Rate.objects.create(
        time=datetime(2022, 12, 13, 8, 19, 11, tzinfo=timezone.utc),
        asset_name="BTC",
        interval=RateInterval.DAILY,
        amount_usd="17169.2180781447",
    )
    yield rate
    rate.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_daily_four():
    rate = Rate.objects.create(
        time=datetime(2013, 7, 14, 0, 0, tzinfo=timezone.utc),
        asset_name="BTC",
        interval=RateInterval.DAILY,
        amount_usd="95.58",
    )
    yield rate
    rate.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_daily_five():
    rate = Rate.objects.create(
        time=datetime(2018, 2, 13, 0, 0, tzinfo=timezone.utc),
        asset_name="BTC",
        interval=RateInterval.DAILY,
        amount_usd="8911.3985742083",
    )
    yield rate
    rate.delete()
