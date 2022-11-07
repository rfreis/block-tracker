import pytest

from protocol.bitcoin import Bitcoin


def _validate_ckd(expected_hashes, derived_hashes):
    content = {
        "receive": {
            "P2PKH": {},
            "P2WPKH": {},
        },
        "change": {
            "P2PKH": {},
            "P2WPKH": {},
        },
    }
    for ckd_address in derived_hashes:
        if ckd_address["is_change"]:
            content["change"][ckd_address["semantic"]][
                ckd_address["index"]
            ] = ckd_address
        else:
            content["receive"][ckd_address["semantic"]][
                ckd_address["index"]
            ] = ckd_address

    for receive_or_change in ["receive", "change"]:
        is_change = receive_or_change == "change"
        for hashes in expected_hashes[receive_or_change]:
            index = hashes["index"]
            derived_data_p2pkh = content[receive_or_change]["P2PKH"][index]
            derived_data_p2wpkh = content[receive_or_change]["P2WPKH"][index]
            assert hashes["p2pkh_address"] == derived_data_p2pkh["address"]
            assert hashes["p2wpkh_address"] == derived_data_p2wpkh["address"]
            assert derived_data_p2pkh["is_change"] == is_change
            assert derived_data_p2wpkh["is_change"] == is_change


def test_ckd_format(ckd_bitcoin_hashes):
    xpub = ckd_bitcoin_hashes["xpub"]
    data = Bitcoin.derive_addresses_from_xpublic_key(xpub, end=0)
    expected_data = [
        {
            "index": 0,
            "address": "1NQpH6Nf8QtR2HphLRcvuVqfhXBXsiWn8r",
            "semantic": "P2PKH",
            "is_change": False,
        },
        {
            "index": 0,
            "address": "bc1qatd6clekcdlrjds3dzm64m3ukf9z2vfdz3hajy",
            "semantic": "P2WPKH",
            "is_change": False,
        },
        {
            "index": 0,
            "address": "1EKtZ7DbxaSB7HB4JtZhmfoc9W8kvd2AtE",
            "semantic": "P2PKH",
            "is_change": True,
        },
        {
            "index": 0,
            "address": "bc1qjgkzss0j03rh37tm5mr3uznedpdx7tzq6me2nw",
            "semantic": "P2WPKH",
            "is_change": True,
        },
    ]
    assert data == expected_data


def test_ckd(ckd_bitcoin_hashes):
    xpub = ckd_bitcoin_hashes["xpub"]
    ckd_addresses = [
        *Bitcoin.derive_addresses_from_xpublic_key(xpub, end=49),
        *Bitcoin.derive_addresses_from_xpublic_key(
            xpub, start=1000000000, end=1000000000
        ),
        *Bitcoin.derive_addresses_from_xpublic_key(
            xpub, start=2147483647, end=2147483647
        ),
    ]
    _validate_ckd(ckd_bitcoin_hashes, ckd_addresses)
