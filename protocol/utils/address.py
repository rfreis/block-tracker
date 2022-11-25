import hashlib

from base58 import b58decode_check, b58encode_check
from protocol.utils import bech32


def validate_base58(address, **kwargs):
    try:
        b58decode_check(address)
    except (ValueError, UnicodeEncodeError):
        return False
    return True


def validate_bech32(address, **kwargs):
    hpr = kwargs["hpr"]
    version, hashed_data = bech32.decode(hpr, address)
    return bool(hashed_data)


def generate_p2pkh(public_key, **kwargs):
    prefix = kwargs["prefix"]
    if prefix.startswith("0x"):
        prefix = prefix[2:]
    pubkey_hash = hashlib.new("ripemd160", hashlib.sha256(public_key).digest()).digest()
    prefix_and_hash = bytes.fromhex(prefix) + pubkey_hash
    return b58encode_check(prefix_and_hash).decode()


def generate_p2wpkh(public_key, **kwargs):
    hpr = kwargs["hpr"]
    version = kwargs["version"]
    if version.startswith("0x"):
        version = version[2:]
        version = int(version, 16)
    address = bech32.encode(
        hpr,
        version,
        hashlib.new("ripemd160", hashlib.sha256(public_key).digest()).digest(),
    )
    return address
