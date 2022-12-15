from aiohttp import ClientSession
from datetime import datetime, timezone

from rate.constants import RateInterval


class CoinGeckoProvider:
    BASE_URL = "https://api.coingecko.com/api/v3"
    asset_ids = {
        "BTC": "bitcoin",
    }

    async def client_request(self, url):
        async with ClientSession() as session:
            async with session.get(url, raise_for_status=True) as response:
                content = await response.json()
                return content

    def _get_daily_history(self, asset_id, days="max"):
        url = f"{self.BASE_URL}/coins/{asset_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
        return self.client_request(url)

    def _format_daily_history(self, content, asset_name):
        formatted_content = []
        for js_timestamp, price in content["prices"]:
            formatted_content.append(
                {
                    "time": datetime.fromtimestamp(
                        js_timestamp / 1000, tz=timezone.utc
                    ),
                    "asset_name": asset_name,
                    "interval": RateInterval.DAILY,
                    "amount_usd": str(price),
                }
            )
        return formatted_content

    async def get_daily_history(self, asset_name, last_price_date=None):
        if last_price_date:
            timedelta_obj = datetime.now(tz=timezone.utc) - last_price_date
            days = timedelta_obj.days
        else:
            days = "max"

        if not days:
            return []

        asset_id = self.asset_ids[asset_name]
        content = await self._get_daily_history(asset_id, days)
        formatted_content = self._format_daily_history(content, asset_name)
        return formatted_content

    def _get_current_price(self, asset_id):
        url = f"{self.BASE_URL}/simple/price?ids={asset_id}&vs_currencies=usd&precision=full"
        return self.client_request(url)

    async def get_current_price(self, asset_name):
        asset_id = self.asset_ids[asset_name]
        content = await self._get_current_price(asset_id)
        price = str(content[asset_id]["usd"])
        formatted_content = {
            "time": datetime.now(tz=timezone.utc),
            "asset_name": asset_name,
            "interval": RateInterval.FIVE_MIN,
            "amount_usd": str(price),
        }
        return formatted_content
