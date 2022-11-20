from celery import shared_task


@shared_task
def new_block_hash(protocol_type, block_hash):
    print(protocol_type)
    print(block_hash)
