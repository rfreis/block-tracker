import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction as db_transaction
from django.db.models import Q

from app.celery import app as celery_app
from protocol import Protocol
from rate.utils import get_usd_rate
from transaction.models import InputData, OutputData, Transaction
from wallet.models import Address
from wallet.utils import derive_remaining_addresses, update_all_balances

logger = logging.getLogger(__name__)


def get_transactions_from_user(user):
    queryset = (
        Transaction.objects.filter(is_orphan=False)
        .order_by("-block_time")
        .filter(
            Q(inputs__user_wallet__user=user)
            | Q(inputs__extended_public_key__user_wallet__user=user)
            | Q(outputs__user_wallet__user=user)
            | Q(outputs__extended_public_key__user_wallet__user=user)
        )
    )
    return queryset.distinct()


def filter_inputs_or_outputs_by_address(inputs_or_outputs, filtered_addresses):
    filtered_items = []
    for item in inputs_or_outputs:
        if item["address"] in filtered_addresses:
            filtered_items.append(item)
    return filtered_items


def create_input_and_output_data(
    transaction, content, attr_name, skip_derivation=False
):
    for item in content:
        address_hash = item.pop("address")
        with db_transaction.atomic():
            address = Address.objects.select_for_update().get(
                hash=address_hash, protocol_type=transaction.protocol_type
            )
            data_queryset = getattr(transaction, attr_name)
            data_obj = data_queryset.filter(address=address)
            if not data_obj:
                item["address"] = address
                data_obj = data_queryset.create(**item)
                if transaction.is_confirmed:
                    update_all_balances(
                        address, item["asset_name"], item["amount_asset"], attr_name
                    )

        if skip_derivation is False and address.extended_public_key:
            derive_remaining_addresses(
                address.extended_public_key,
                address.details["semantic"],
                address.is_change,
            )


def add_usd_rates_to_inputs_outputs(data_items, block_time):
    for data_item in data_items:
        data_item["amount_usd"] = get_usd_rate(
            data_item["asset_name"], data_item["amount_asset"], block_time
        )


def create_transactions(formatted_txs, protocol_type, skip_derivation=False):
    for tx in formatted_txs:
        tx_addresses = tx.pop("addresses")
        tx_addresses = [address.replace("\x00", "0x00") for address in tx_addresses]
        filtered_addresses = list(
            Address.objects.filter(
                protocol_type=protocol_type, hash__in=tx_addresses
            ).values_list("hash", flat=True)
        )
        if not filtered_addresses:
            continue

        inputs = tx.pop("inputs")
        add_usd_rates_to_inputs_outputs(inputs, tx["block_time"])
        tx["details"]["inputs"] = json.loads(json.dumps(inputs, cls=DjangoJSONEncoder))
        outputs = tx.pop("outputs")
        add_usd_rates_to_inputs_outputs(outputs, tx["block_time"])
        tx["details"]["outputs"] = json.loads(
            json.dumps(outputs, cls=DjangoJSONEncoder)
        )
        tx["details"]["value_input_usd"] = get_usd_rate(
            tx["details"]["asset_name"], tx["details"]["value_input"], tx["block_time"]
        )
        tx["details"]["value_output_usd"] = get_usd_rate(
            tx["details"]["asset_name"], tx["details"]["value_output"], tx["block_time"]
        )
        tx["details"]["fee_usd"] = get_usd_rate(
            tx["details"]["asset_name"], tx["details"]["fee"], tx["block_time"]
        )
        filtered_inputs = filter_inputs_or_outputs_by_address(
            inputs, filtered_addresses
        )
        filtered_outputs = filter_inputs_or_outputs_by_address(
            outputs, filtered_addresses
        )

        logger.debug(
            "Creating transaction for protocol %s %s" % (protocol_type, tx["tx_id"])
        )
        transaction = Transaction.objects.filter(
            protocol_type=protocol_type,
            tx_id=tx["tx_id"],
        )
        if transaction:
            transaction = transaction.first()
        else:
            transaction = Transaction.objects.create(**tx)

        create_input_and_output_data(
            transaction, filtered_inputs, "inputdata", skip_derivation=skip_derivation
        )
        create_input_and_output_data(
            transaction, filtered_outputs, "outputdata", skip_derivation=skip_derivation
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


def sync_empty_usd_rates():
    data_models = [InputData, OutputData]
    for DataModel in data_models:
        queryset = DataModel.objects.filter(amount_usd__isnull=True)
        logger.debug(
            "Found %s %s with empty amount_usd" % (queryset.count(), DataModel)
        )
        for data_obj in queryset:
            amount_usd = get_usd_rate(
                data_obj.asset_name,
                data_obj.amount_asset,
                data_obj.transaction.block_time,
            )
            if amount_usd:
                data_obj.amount_usd = amount_usd
                data_obj.save(update_fields=["amount_usd"])
                logger.debug("Added amount_usd to %s #%s" % (DataModel, data_obj.id))


def confirm_transactions(transactions):
    transaction_ids = list(transactions.values_list("id", flat=True))
    str_transaction_ids = ", ".join(str(x) for x in transaction_ids)
    logger.info(
        "Found %s (%s) new confirmed transactions."
        % (transactions.count(), str_transaction_ids)
    )
    for transaction in transactions:
        logger.debug(
            "Confirming transaction for protocol %s %s"
            % (transaction.protocol_type, transaction.tx_id)
        )
        with db_transaction.atomic():
            for attr_name in ["inputdata", "outputdata"]:
                for item_obj in getattr(transaction, attr_name).all():
                    address = Address.objects.select_for_update().get(
                        id=item_obj.address.id
                    )
                    update_all_balances(
                        address,
                        item_obj.asset_name,
                        item_obj.amount_asset,
                        attr_name,
                    )
            transaction.is_confirmed = True
            transaction.save(update_fields=["is_confirmed"])
    celery_app.send_task(
        "transaction.tasks.new_confirmed_transactions", (transaction_ids,)
    )
