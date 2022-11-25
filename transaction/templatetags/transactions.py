from decimal import Decimal

from django import template
from django.db.models import Q


register = template.Library()


@register.filter(name="transaction_balance")
def transaction_balance(transaction, user_wallets):
    inputs = transaction.inputdata.filter(
        Q(address__user_wallet__in=user_wallets)
        | Q(address__extended_public_key__user_wallet__id__in=user_wallets)
    )
    outputs = transaction.outputdata.filter(
        Q(address__user_wallet__in=user_wallets)
        | Q(address__extended_public_key__user_wallet__id__in=user_wallets)
    )
    balances = {}
    for _input in inputs:
        if _input.asset_name not in balances:
            balances[_input.asset_name] = Decimal("0")
        balances[_input.asset_name] -= Decimal(_input.amount_asset)

    for output in outputs:
        if output.asset_name not in balances:
            balances[output.asset_name] = Decimal("0")
        balances[output.asset_name] += Decimal(output.amount_asset)

    return balances
