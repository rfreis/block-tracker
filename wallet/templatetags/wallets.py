from datetime import datetime, timezone
from decimal import Decimal

from django import template

from rate.utils import get_usd_rate

register = template.Library()


@register.filter(name="wallet_balance_usd")
def wallet_balance_usd(address_or_extended_public_key):
    total = Decimal("0")
    now = datetime.now(tz=timezone.utc)
    for asset_name, asset_amount in address_or_extended_public_key.balance.items():
        asset_usd = get_usd_rate(asset_name, asset_amount, now)
        if asset_usd:
            total += Decimal(asset_usd)
    return total
