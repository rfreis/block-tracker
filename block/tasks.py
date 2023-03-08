import logging

from app.celery import app as celery_app
from block.utils import sync_chain_of_blocks
from protocol.utils.exceptions import ClientException

logger = logging.getLogger(__name__)


@celery_app.task(
    autoretry_for=(ClientException,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def new_block_hash(protocol_type, block_hash):
    logger.info("New block hash %s for protocol %s" % (block_hash, protocol_type))
    sync_chain_of_blocks(protocol_type)
