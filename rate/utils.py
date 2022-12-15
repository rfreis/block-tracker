import asyncio
from datetime import timedelta
from decimal import Decimal

from rate.constants import RateInterval
from rate.models import Rate
from rate.provider.coingecko import CoinGeckoProvider


async def fetch_rates(last_price_date):
    provider = CoinGeckoProvider()

    daily_history_content, current_price_content = await asyncio.gather(
        provider.get_daily_history("BTC", last_price_date),
        provider.get_current_price("BTC"),
    )

    return [*daily_history_content, current_price_content]


def sync_rates():
    last_daily_price = (
        Rate.objects.filter(asset_name="BTC", interval=RateInterval.DAILY)
        .order_by("-time")
        .first()
    )
    last_price_date = None if not last_daily_price else last_daily_price.time

    content = asyncio.run(fetch_rates(last_price_date))

    for rate_data in content:
        Rate.objects.create(**rate_data)


def get_usd_rate(asset_name, amount_asset, time_reference):
    limit_time_reference = time_reference - timedelta(days=1)
    last_price = (
        Rate.objects.filter(
            asset_name=asset_name,
            time__lte=time_reference,
            time__gte=limit_time_reference,
        )
        .order_by("-time")
        .first()
    )

    if not last_price:
        return None

    return str(Decimal(amount_asset) * Decimal(last_price.amount_usd))
