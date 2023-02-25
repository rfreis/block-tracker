import logging
from decimal import Decimal

from django.db.models import Count, Q

from accounts.models import User
from dashboard.utils import get_or_create_last_user_balance
from protocol import Protocol
from wallet.models import Address, ExtendedPublicKey


logger = logging.getLogger(__name__)


def get_last_address_index_from_extended_public_key(
    extended_public_key, filters={}, only_used_addresses=False
):
    queryset = Address.objects.filter(extended_public_key=extended_public_key)
    if filters:
        queryset = queryset.filter(**filters)
    if only_used_addresses:
        queryset = queryset.annotate(
            inputs_qty=Count("inputs"), outputs_qty=Count("outputs")
        ).filter(Q(inputs_qty__gt=0) | Q(outputs_qty__gt=0))

    queryset = queryset.values("index")

    if not queryset:
        return None

    last_address_by_index = queryset.order_by("-index").first()

    return last_address_by_index["index"]


def derive_addresses_from_extended_public_key(
    extended_public_key, start=0, end=20, **kwargs
):
    protocol = Protocol(extended_public_key.protocol_type)
    addresses = protocol.derive_addresses_from_xpublic_key(
        extended_public_key.hash, start=start, end=end, **kwargs
    )

    for address in addresses:
        Address.objects.create(
            extended_public_key=extended_public_key,
            protocol_type=extended_public_key.protocol_type,
            hash=address["address"],
            is_change=address.get("is_change", False),
            index=address["index"],
            details={"semantic": address.get("semantic", None)},
        )


def derive_remaining_addresses(extended_public_key, semantic, is_change, index=None):
    if index is not None and index <= 0:
        return

    last_index = get_last_address_index_from_extended_public_key(
        extended_public_key,
        filters={
            "is_change": is_change,
            "details__semantic": semantic,
        },
    )
    start = last_index + 1 if last_index is not None else 0
    if index:
        end = index + 20
    else:
        last_used_index = get_last_address_index_from_extended_public_key(
            extended_public_key,
            filters={
                "is_change": is_change,
                "details__semantic": semantic,
            },
            only_used_addresses=True,
        )
        end = last_used_index + 20 if last_used_index is not None else 20
    if end > start:
        derive_addresses_from_extended_public_key(
            extended_public_key,
            start=start,
            end=end,
            semantic=semantic,
            is_change=is_change,
        )


def update_balance(obj, asset_name, amount, attr_name):
    logger.debug(
        "Updating balance for %s (#%s). %s %s (%s)"
        % (obj, obj.id, amount, asset_name, attr_name)
    )
    prev_balance = Decimal(obj.balance.get(asset_name, "0.00"))
    if attr_name == "inputdata":
        new_balance = prev_balance - Decimal(amount)
    else:
        new_balance = prev_balance + Decimal(amount)
    obj.balance[asset_name] = str(new_balance)
    obj.save()
    logger.debug(
        "Updated balance for %s (#%s). %s %s (%s)"
        % (obj, obj.id, amount, asset_name, attr_name)
    )


def update_all_balances(address, asset_name, amount, attr_name):
    update_balance(address, asset_name, amount, attr_name)
    user_filters = Q(user_wallet__address=address)
    if address.extended_public_key:
        extended_public_key = ExtendedPublicKey.objects.select_for_update().get(
            id=address.extended_public_key.id
        )
        update_balance(extended_public_key, asset_name, amount, attr_name)
        user_filters.add(Q(user_wallet__extended_public_key=extended_public_key), Q.OR)

    users = User.objects.filter(user_filters)
    for user in users:
        user_balance = get_or_create_last_user_balance(user, for_update=True)
        update_balance(user_balance, asset_name, amount, attr_name)
