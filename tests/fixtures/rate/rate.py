from datetime import datetime, timezone

import pytest  # noqa: F401

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


@pytest.fixture
@pytest.mark.usefixtures("db")
def rate_bitcoin_history():
    rates = [
        Rate(
            time=datetime(2022, 1, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="37983.151499406464",
        ),
        Rate(
            time=datetime(2022, 2, 28, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="37803.59016044929",
        ),
        Rate(
            time=datetime(2022, 3, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="47063.36584996355",
        ),
        Rate(
            time=datetime(2022, 4, 30, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="38650.55013809267",
        ),
        Rate(
            time=datetime(2022, 5, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="31740.94072516695",
        ),
        Rate(
            time=datetime(2022, 6, 30, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="20108.529472889782",
        ),
        Rate(
            time=datetime(2022, 7, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="23653.459549430798",
        ),
        Rate(
            time=datetime(2022, 8, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="19805.35069885804",
        ),
        Rate(
            time=datetime(2022, 9, 30, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="19563.765161776904",
        ),
        Rate(
            time=datetime(2022, 10, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="20623.871497040946",
        ),
        Rate(
            time=datetime(2022, 11, 30, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="16441.979978419113",
        ),
        Rate(
            time=datetime(2022, 12, 31, 0, 0, tzinfo=timezone.utc),
            asset_name="BTC",
            interval=RateInterval.DAILY,
            amount_usd="16604.020520373393",
        ),
    ]

    rates = Rate.objects.bulk_create(rates)

    yield rates

    for rate in rates:
        rate.delete()
