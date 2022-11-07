from protocol import Protocol

from transaction.models import Transaction
from wallet.models import Address
from wallet.utils import derive_remaining_addresses


def create_input_and_output_data(transaction, content, attr_name):
    for item in content:
        address_hash = item.pop("address")
        item["address"] = Address.objects.get(
            hash=address_hash, protocol_type=transaction.protocol_type
        )
        data_queryset = getattr(transaction, attr_name)
        data_obj = data_queryset.filter(address=item["address"])
        if data_obj:
            data_obj = data_obj.first()
        else:
            data_obj = data_queryset.create(**item)


def sync_transactions_from_extended_public_key(extended_public_key):
    protocol = Protocol(extended_public_key.protocol_type)
    content = protocol.get_transactions_from_xpublic_key(extended_public_key.hash)
    if not content:
        return

    last_used_indexes = content["last_used_indexes"]
    for semantic, last_used_index in last_used_indexes.items():
        derive_remaining_addresses(
            extended_public_key, semantic, last_used_index["receive"], False
        )
        derive_remaining_addresses(
            extended_public_key, semantic, last_used_index["change"], True
        )

    transactions = content["txs"]
    for tx in transactions:
        transaction = Transaction.objects.filter(
            protocol_type=extended_public_key.protocol_type,
            tx_id=tx["tx_id"],
        )
        inputs = tx.pop("inputs")
        outputs = tx.pop("outputs")
        if transaction:
            transaction = transaction.first()
        else:
            transaction = Transaction.objects.create(**tx)

        create_input_and_output_data(transaction, inputs, "inputdata")
        create_input_and_output_data(transaction, outputs, "outputdata")
