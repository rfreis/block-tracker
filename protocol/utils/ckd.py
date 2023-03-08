import hashlib
import hmac

import ecdsa
from base58 import b58encode_check

CURVE_GEN = ecdsa.ecdsa.generator_secp256k1
CURVE_ORDER = CURVE_GEN.order()


def child_xpub_derivation(child_index, parent_deserialized_key):
    assert child_index < 2**31  # if index > 0x80000000 = hardened derivation

    child_index_bytes = child_index.to_bytes(4, "big")
    data = parent_deserialized_key["key"] + child_index_bytes

    I = hmac.new(  # noqa: E741
        parent_deserialized_key["chaincode"], data, hashlib.sha512
    ).digest()
    Ileft, Iright = I[:32], I[32:]
    child_chaincode = Iright

    Ileft_parsed = ecdsa.ecdsa.string_to_int(Ileft)
    if Ileft_parsed >= CURVE_ORDER:
        return False, {}, None

    parent_key = ecdsa.VerifyingKey.from_string(
        parent_deserialized_key["key"], curve=ecdsa.curves.SECP256k1
    )
    child_key_point = Ileft_parsed * CURVE_GEN + parent_key.pubkey.point
    if child_key_point == ecdsa.ellipticcurve.INFINITY:
        return False, {}, None

    child_key = ecdsa.VerifyingKey.from_public_point(
        child_key_point, curve=ecdsa.curves.SECP256k1
    )
    if child_key.pubkey.point.y() & 1:
        child_key_data = b"\3" + ecdsa.ecdsa.int_to_string(child_key.pubkey.point.x())
    else:
        child_key_data = b"\2" + ecdsa.ecdsa.int_to_string(child_key.pubkey.point.x())

    child_fingerprint = hashlib.new(
        "ripemd160", hashlib.sha256(parent_deserialized_key["key"]).digest()
    ).digest()[:4]
    child_depth_int = int.from_bytes(parent_deserialized_key["depth"], "big") + 1
    child_depth = child_depth_int.to_bytes(1, "big")
    child_deserialized_key = {
        "version": parent_deserialized_key["version"],
        "depth": child_depth,
        "fingerprint": child_fingerprint,
        "index": child_index_bytes,
        "chaincode": child_chaincode,
        "key": child_key_data,
    }
    decoded_xpub = (
        child_deserialized_key["version"]
        + child_deserialized_key["depth"]
        + child_deserialized_key["fingerprint"]
        + child_deserialized_key["index"]
        + child_deserialized_key["chaincode"]
        + child_deserialized_key["key"]
    )
    encoded_xpub = b58encode_check(decoded_xpub)

    return True, child_deserialized_key, encoded_xpub
