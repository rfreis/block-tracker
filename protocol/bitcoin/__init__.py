from protocol.base import ProtocolBase
from protocol.bitcoin.backend_blockbook import BitcoinBlockBookMixin
from protocol.bitcoin.ckd import BitcoinCKDMixin
from protocol.bitcoin.validate import BitcoinValidateMixin
from protocol.bitcoin.websocket_blockbook import BitcoinSocketIOMixin
from protocol.utils.address import (
    generate_p2pkh,
    generate_p2wpkh,
    validate_base58,
    validate_bech32,
)
from protocol.utils.xpublic_key import validate_xpub

__all__ = ["Bitcoin", "BitcoinTestnet"]


class BitcoinBase(
    BitcoinBlockBookMixin,
    BitcoinValidateMixin,
    BitcoinCKDMixin,
    ProtocolBase,
    BitcoinSocketIOMixin,
):
    required_confirmations = 6
    addresses = {}
    extended_pubkeys = {}
    hashblock_event_name = "bitcoind/hashblock"


class Bitcoin(BitcoinBase):
    asset_name = "BTC"
    addresses = {
        "P2PKH": {
            "leading_symbols": ["1"],
            "generate_function": generate_p2pkh,
            "validate_function": validate_base58,
            "kwargs": {
                "prefix": "0x00",
            },
        },
        "P2WPKH": {
            "leading_symbols": ["bc1"],
            "generate_function": generate_p2wpkh,
            "validate_function": validate_bech32,
            "kwargs": {
                "hpr": "bc",
                "version": "0x00",
            },
        },
    }
    extended_pubkeys = {
        "xpub": {
            "address_semantics": ["P2PKH", "P2WPKH"],
            "prefix": "0x0488B21E",
            "leading_symbols": ["xpub"],
            "validate_function": validate_xpub,
        },
    }


class BitcoinTestnet(BitcoinBase):
    asset_name = "BTCTEST"
    addresses = {
        "P2PKH": {
            "leading_symbols": ["m", "n"],
            "generate_function": generate_p2pkh,
            "validate_function": validate_base58,
            "kwargs": {
                "prefix": "0x6F",
            },
        },
        "P2WPKH": {
            "leading_symbols": ["tb1"],
            "generate_function": generate_p2wpkh,
            "validate_function": validate_bech32,
            "kwargs": {
                "hpr": "tb",
                "version": "0x00",
            },
        },
    }
    extended_pubkeys = {
        "tpub": {
            "address_semantics": ["P2PKH", "P2WPKH"],
            "prefix": "0x043587CF",
            "leading_symbols": ["tpub"],
            "validate_function": validate_xpub,
        },
    }
