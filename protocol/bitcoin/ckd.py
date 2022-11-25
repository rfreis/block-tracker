from protocol.utils.xpublic_key import deserialize_xpub
from protocol.utils.ckd import child_xpub_derivation


class BitcoinCKDMixin:
    @staticmethod
    def deserialize_xpublic_key(xpublic_key):
        is_valid, deserialized_xpub = deserialize_xpub(xpublic_key)
        if not is_valid:
            return None
        return deserialized_xpub

    @staticmethod
    def ckd_by_index(deserialized_xpub, index):
        is_valid, deserialized_child_key, child_xpub = child_xpub_derivation(
            index,
            deserialized_xpub,
        )
        if not is_valid:
            return None, None

        return deserialized_child_key, child_xpub

    @classmethod
    def encode_address_from_public_key(cls, public_key, semantic):
        data = cls.addresses[semantic]
        generate_function = data["generate_function"]
        return generate_function(public_key, **data.get("kwargs", {}))

    @classmethod
    def _generate_addresses_from_deserialized_chain_key(
        cls, deserialized_public_key, semantics, start_index, end_index
    ):
        addresses = []

        for child_index in range(start_index, end_index + 1):
            child_public_key_deserialized, child_xpub = cls.ckd_by_index(
                deserialized_public_key,
                child_index,
            )
            for semantic in semantics:
                address = cls.encode_address_from_public_key(
                    child_public_key_deserialized["key"], semantic
                )
                if address:
                    addresses.append(
                        {
                            "index": child_index,
                            "address": address,
                            "semantic": semantic,
                        }
                    )

        return addresses

    @classmethod
    def _derive_addresses_from_deserialized_parent_key(
        cls, deserialized_xpub, semantics, is_change=False, start=0, end=20
    ):
        child_index = 1 if is_change else 0
        child_deserialized_xpub, xpub = cls.ckd_by_index(
            deserialized_xpub,
            child_index,
        )
        if not xpub:
            raise Exception("Invalid derivation key")

        addresses = cls._generate_addresses_from_deserialized_chain_key(
            child_deserialized_xpub,
            semantics,
            start,
            end,
        )

        for address in addresses:
            address["is_change"] = is_change

        return addresses

    @classmethod
    def derive_addresses_from_xpublic_key(
        cls, xpublic_key, semantics=[], start=0, end=19, **kwargs
    ):
        deserialized_xpub = cls.deserialize_xpublic_key(xpublic_key)
        if not deserialized_xpub:
            raise Exception("Invalid extended public key")

        semantics = semantics if semantics else cls.addresses.keys()
        if kwargs.get("semantic"):
            semantics = [kwargs.get("semantic")]

        content = []
        if not kwargs.get("is_change", False):
            receive_addresses = cls._derive_addresses_from_deserialized_parent_key(
                deserialized_xpub,
                semantics,
                is_change=False,
                start=start,
                end=end,
            )
            content += receive_addresses

        if kwargs.get("is_change", True):
            change_addresses = cls._derive_addresses_from_deserialized_parent_key(
                deserialized_xpub,
                semantics,
                is_change=True,
                start=start,
                end=end,
            )
            content += change_addresses

        return content
