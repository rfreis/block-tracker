import os
from datetime import datetime, timezone
from decimal import Decimal

from protocol.utils.blockbook import BlockBookClient


BLOCKBOOK_SETTINGS = {
    "Bitcoin": {
        "url": os.environ.get("BITCOIN_BLOCKBOOK_URL", ""),
    },
    "BitcoinTestnet": {
        "url": os.environ.get("BITCOIN_TESTNET_BLOCKBOOK_URL", ""),
    },
}


class BitcoinBlockBookMixin:
    _decimal_places = 8
    _divisible_by = None

    def __init__(self, *args, **kwargs):
        blockbook_settings = BLOCKBOOK_SETTINGS[self.__class__.__name__]
        self.backend = BlockBookClient(blockbook_settings["url"])
        super().__init__(*args, **kwargs)

    @property
    def divisible_by(self):
        if not self._divisible_by:
            self._divisible_by = 10**self._decimal_places
        return self._divisible_by

    def _format_value(self, value):
        return Decimal(str(int(value) / self.divisible_by))

    def _format_txs(self, txs):
        formatted_txs = []
        for tx in txs:
            is_confirmed = tx["confirmations"] >= self.required_confirmations
            block_time = datetime.fromtimestamp(tx["blockTime"], tz=timezone.utc)
            formatted_tx = {
                "protocol_type": self.protocol_type,
                "tx_id": tx["txid"],
                "block_id": tx["blockHeight"],
                "block_time": block_time,
                "is_confirmed": is_confirmed,
                "details": {
                    "value_input": str(self._format_value(tx["valueIn"])),
                    "value_output": str(self._format_value(tx["value"])),
                    "fee": str(self._format_value(tx["fees"])),
                    "block_hash": tx["blockHash"],
                },
            }
            vins = []
            for vin in tx["vin"]:
                if vin.get("isOwn"):
                    vins.append(
                        {
                            "amount_asset": self._format_value(vin["value"]),
                            "asset_name": self.asset_name,
                            "address": vin["addresses"][0],
                        }
                    )
            vouts = []
            for vout in tx["vout"]:
                if vout.get("isOwn"):
                    vouts.append(
                        {
                            "amount_asset": self._format_value(vout["value"]),
                            "asset_name": self.asset_name,
                            "address": vout["addresses"][0],
                        }
                    )
            formatted_tx["inputs"] = vins
            formatted_tx["outputs"] = vouts
            formatted_txs.append(formatted_tx)
        return formatted_txs

    def get_current_block(self):
        content = self.backend.get_current_block()
        return content["blockbook"]["bestHeight"]

    def get_last_used_address(self, addresses):
        if not addresses:
            return None

        last_address_index = {
            "receive": 0,
            "change": 0,
        }
        for address in addresses:
            split_path = address["path"].split("/")
            change = int(split_path[-2])
            key = "receive" if change == 0 else "change"
            index = int(split_path[-1])
            if last_address_index[key] < index:
                last_address_index[key] = index

        return last_address_index

    def get_transactions_from_xpublic_key(self, xpublic_key):
        is_valid, xpub_semantic = self.validate_xpublic_key(xpublic_key)
        if not is_valid:
            return None

        address_semantics = self.extended_pubkeys[xpub_semantic]["address_semantics"]
        txs = []
        last_used_indexes = {}
        for address_semantic in address_semantics:
            content = self.backend.get_xpub(
                xpublic_key,
                address_semantic=address_semantic,
                details="txs",
                tokens="used",
            )
            if content.get("transactions"):
                last_used_index = self.get_last_used_address(content["tokens"])
                last_used_indexes[address_semantic] = last_used_index
                txs += content["transactions"]

        if not txs:
            return None

        formatted_txs = self._format_txs(txs)

        return {"txs": formatted_txs, "last_used_indexes": last_used_indexes}
