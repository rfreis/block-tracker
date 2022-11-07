from ecdsa import VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa.errors import MalformedPointError
from base58 import b58decode_check


def validate_deserialized_xpub(deserialized_xpub):
    public_key = deserialized_xpub["key"]

    if not public_key.startswith(b"\3") and not public_key.startswith(b"\2"):
        return False

    if (
        deserialized_xpub["depth"] == b"\x00"
        and deserialized_xpub["fingerprint"] != b"\x00\x00\x00\x00"
    ):
        return False

    if (
        deserialized_xpub["depth"] == b"\x00"
        and deserialized_xpub["index"] != b"\x00\x00\x00\x00"
    ):
        return False

    try:
        VerifyingKey.from_string(public_key, curve=SECP256k1)
    except MalformedPointError:
        return False

    return True


def deserialize_xpub(xpub):
    try:
        decoded_xpub = b58decode_check(xpub)
    except (ValueError, UnicodeEncodeError):
        return False, {}

    version = decoded_xpub[:4]
    depth = decoded_xpub[4:5]
    fingerprint = decoded_xpub[5:9]
    index = decoded_xpub[9:13]
    chaincode = decoded_xpub[13:45]
    key = decoded_xpub[45:]

    deserialized_xpub = {
        "version": version,
        "depth": depth,
        "fingerprint": fingerprint,
        "index": index,
        "chaincode": chaincode,
        "key": key,
    }

    is_valid = validate_deserialized_xpub(deserialized_xpub)

    return is_valid, deserialized_xpub


def validate_xpub(xpub, **kwargs):
    is_valid, _ = deserialize_xpub(xpub)
    return is_valid
