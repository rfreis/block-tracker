import logging

from block.models import Block
from protocol import Protocol
from transaction.models import Transaction
from transaction.utils import confirm_transactions, create_transactions

logger = logging.getLogger(__name__)


def confirm_blocks(protocol_type, last_confirmed_block_id):
    transactions = Transaction.objects.filter(
        protocol_type=protocol_type,
        block_id__lte=last_confirmed_block_id,
        is_confirmed=False,
        is_orphan=False,
    )
    if transactions:
        confirm_transactions(transactions)

    blocks = Block.objects.filter(
        protocol_type=protocol_type,
        block_id__lte=last_confirmed_block_id,
        is_confirmed=False,
        is_orphan=False,
    )
    if blocks:
        block_ids = ", ".join(str(x) for x in list(blocks.values_list("id", flat=True)))
        logger.info("Found %s (%s) new confirmed blocks." % (blocks.count(), block_ids))
        blocks.update(is_confirmed=True)


def make_block_orphan(block):
    transactions = Transaction.objects.filter(
        protocol_type=block.protocol_type,
        block_id=block.block_id,
    )
    if transactions:
        transaction_ids = ", ".join(
            str(x) for x in list(transactions.values_list("id", flat=True))
        )
        logger.info(
            "Found %s (%s) orphan transactions on orphan block #%s."
            % (transactions.count(), transaction_ids, block.id)
        )
        transactions.update(is_orphan=True)

    block.is_orphan = True
    block.save(update_fields=["is_orphan"])


def check_orphan_blocks(protocol_type, block_id=None):
    if block_id:
        block = Block.objects.get(
            protocol_type=protocol_type,
            block_id=block_id,
            is_orphan=False,
        )
    else:
        block = Block.objects.filter(
            protocol_type=protocol_type,
            is_orphan=False,
        ).order_by("-block_id")
        if not block:
            return
        block = block.first()

    protocol = Protocol(protocol_type)
    block_hash = protocol.get_block_hash(block.block_id)
    if block_hash == block.block_hash:
        return

    if block.is_confirmed:
        logger.critical(
            "Confirmed block %s is orphan for protocol %s" % (block_id, protocol_type)
        )
        raise Exception("Critical: confirmed block is orphan")

    logger.info("Found orphan block #%s." % block.id)
    make_block_orphan(block)
    next_block_id = block.block_id - 1
    check_orphan_blocks(protocol_type, next_block_id)


def digest_new_block(protocol_type, last_confirmed_block_id, block_id):
    protocol = Protocol(protocol_type)
    content = protocol.get_block(block_id)

    all_transactions = content.pop("txs")

    create_transactions(all_transactions, protocol_type)

    is_confirmed = last_confirmed_block_id >= block_id
    Block.objects.create(
        protocol_type=protocol_type, is_confirmed=is_confirmed, **content
    )


def sync_chain_of_blocks(protocol_type, block_id=None):
    logger.debug("Start of sync_chain_of_blocks (%s, %s)" % (protocol_type, block_id))
    check_orphan_blocks(protocol_type)

    protocol = Protocol(protocol_type)
    current_block = block_id if block_id else protocol.get_current_block()
    last_block = Block.objects.filter(
        protocol_type=protocol_type,
        is_orphan=False,
    ).order_by("-block_id")
    if last_block:
        last_block = last_block.first()
        last_block_id = last_block.block_id + 1
    else:
        last_block_id = current_block
    last_confirmed_block = current_block + 1 - protocol.required_confirmations

    for block_height in range(last_block_id, current_block + 1):
        digest_new_block(protocol_type, last_confirmed_block, block_height)

    confirm_blocks(protocol_type, last_confirmed_block)
    logger.debug("End of sync_chain_of_blocks (%s, %s)" % (protocol_type, block_id))
