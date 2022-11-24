from django.db.models import Count, Q

from protocol import Protocol

from wallet.models import Address


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
