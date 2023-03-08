import os

from protocol.utils.blockbook import BlockBookSocketIOClient

BLOCKBOOK_SETTINGS = {
    "Bitcoin": {
        "url": os.environ.get("BITCOIN_BLOCKBOOK_WEBSOCKET", ""),
    },
    "BitcoinTestnet": {
        "url": os.environ.get("BITCOIN_TESTNET_BLOCKBOOK_WEBSOCKET", ""),
    },
}


class BitcoinSocketIOMixin:
    def __init__(self, *args, **kwargs):
        blockbook_settings = BLOCKBOOK_SETTINGS[self.__class__.__name__]
        self.wss_backend = BlockBookSocketIOClient(
            blockbook_settings["url"],
            self.protocol_type,
            self.hashblock_event_name,
        )
        super().__init__(*args, **kwargs)
