from protocol import Protocol

from wallet.models import Address


def get_last_address_index_from_extended_public_key(extended_public_key, filters={}):
    queryset = Address.objects.filter(extended_public_key=extended_public_key)
    if filters:
        queryset = queryset.filter(**filters)

    queryset = queryset.values("index")

    if not queryset:
        return 0

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


def derive_remaining_addresses(extended_public_key, semantic, index, is_change):
    if index > 0:
        last_index = get_last_address_index_from_extended_public_key(
            extended_public_key,
            filters={
                "is_change": is_change,
                "details__semantic": semantic,
            },
        )
        start = last_index + 1 if last_index else 0
        end = index + 20
        if end > start:
            derive_addresses_from_extended_public_key(
                extended_public_key,
                start=start,
                end=end,
                semantic=semantic,
                is_change=is_change,
            )
