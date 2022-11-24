from protocol import Protocol

from transaction.models import Transaction
from wallet.models import Address
from wallet.utils import derive_remaining_addresses


def create_input_and_output_data(
    transaction, content, attr_name, skip_derivation=False
):
    for item in content:
        address_hash = item.pop("address")
        address = Address.objects.get(
            hash=address_hash, protocol_type=transaction.protocol_type
        )
        if skip_derivation == False and address.extended_public_key:
            derive_remaining_addresses(
                address.extended_public_key,
                address.details["semantic"],
                address.is_change,
            )
        item["address"] = address
        data_queryset = getattr(transaction, attr_name)
        data_obj = data_queryset.filter(address=item["address"])
        if data_obj:
            data_obj = data_obj.first()
        else:
            data_obj = data_queryset.create(**item)


def create_transactions(formatted_txs, protocol_type, skip_derivation=False):
    for tx in formatted_txs:
        transaction = Transaction.objects.filter(
            protocol_type=protocol_type,
            tx_id=tx["tx_id"],
        )
        inputs = tx.pop("inputs")
        outputs = tx.pop("outputs")
        if transaction:
            transaction = transaction.first()
        else:
            transaction = Transaction.objects.create(**tx)

        create_input_and_output_data(
            transaction, inputs, "inputdata", skip_derivation=skip_derivation
        )
        create_input_and_output_data(
            transaction, outputs, "outputdata", skip_derivation=skip_derivation
        )


def sync_transactions_from_address(address):
    protocol = Protocol(address.protocol_type)
    transactions = protocol.get_transactions_from_address(address.hash)
    if not transactions:
        return

    create_transactions(transactions, address.protocol_type)


def sync_transactions_from_extended_public_key(extended_public_key):
    protocol = Protocol(extended_public_key.protocol_type)
    content = protocol.get_transactions_from_xpublic_key(extended_public_key.hash)
    if not content:
        return

    last_used_indexes = content["last_used_indexes"]
    for semantic, last_used_index in last_used_indexes.items():
        derive_remaining_addresses(
            extended_public_key, semantic, False, last_used_index["receive"]
        )
        derive_remaining_addresses(
            extended_public_key, semantic, True, last_used_index["change"]
        )

    transactions = content["txs"]
    create_transactions(
        transactions, extended_public_key.protocol_type, skip_derivation=True
    )
