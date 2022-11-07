import asyncio
from aiohttp import (
    ClientSession,
    ClientError,
)
from urllib.parse import urlencode

from protocol.utils.exceptions import ClientException


class BlockBookClient:
    v2_base = "api/v2"

    def __init__(self, url, timeout=300):
        self.url = url
        self.timeout = timeout

    async def client_request(self, paths, data={}):
        url = self.format_url(paths, data)
        async with ClientSession() as session:
            try:
                async with session.get(
                    url, timeout=self.timeout, raise_for_status=True
                ) as response:
                    content = await response.json()
            except ClientError as exc:
                raise ClientException(str(exc))

            return content

    def format_semantic(self, xpublic_hash, address_semantic=None):
        address_semantic_map = {"P2PKH": ["pkh(", ")"], "P2WPKH": ["wpkh(", ")"]}
        if address_semantic_map.get(address_semantic):
            before, after = address_semantic_map[address_semantic]
            return f"{before}{xpublic_hash}{after}"
        return xpublic_hash

    def format_url(self, paths=[], querystring_data={}):
        url = f"{self.url}/{self.v2_base}"
        if isinstance(paths, str):
            paths = [paths]
        for path in paths:
            url += f"/{path}"
        if querystring_data:
            encoded_querystring = urlencode(querystring_data)
            url += f"?{encoded_querystring}"
        return url

    def get_address(self, address, **data):
        paths = ["address", address]
        return asyncio.run(self.client_request(paths, data))

    def get_block(self, block_height_or_hash, **data):
        paths = ["block", block_height_or_hash]
        return asyncio.run(self.client_request(paths, data))

    def get_current_block(self):
        return asyncio.run(self.client_request(""))

    def get_transaction(self, tx_id, **data):
        paths = ["tx", tx_id]
        return asyncio.run(self.client_request(paths, data))

    def get_xpub(self, xpub_hash, address_semantic=None, **data):
        format_xpub_hash = self.format_semantic(
            xpub_hash, address_semantic=address_semantic
        )
        paths = ["xpub", format_xpub_hash]
        return asyncio.run(self.client_request(paths, data))
