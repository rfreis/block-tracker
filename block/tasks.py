from celery import shared_task
import logging

from block.utils import sync_chain_of_blocks


logger = logging.getLogger(__name__)


@shared_task
def new_block_hash(protocol_type, block_hash):
    logger.info("New block hash %s for protocol %s" % (block_hash, protocol_type))
    sync_chain_of_blocks(protocol_type)
