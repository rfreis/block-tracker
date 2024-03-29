class ProtocolBase:
    protocol_type = None

    def __init__(self, protocol_type=None, *args, **kwargs):
        self.protocol_type = protocol_type
        super().__init__(*args, **kwargs)

    @classmethod
    def validate_address(cls, address):  # pragma: no cover
        raise NotImplementedError("Method not implemented")

    @classmethod
    def validate_xpublic_key(cls, xpublic_key):  # pragma: no cover
        raise NotImplementedError("Method not implemented")

    @classmethod
    def derive_addresses_from_xpublic_key(
        cls, xpublic_key, start=0, end=20, **kwargs
    ):  # pragma: no cover
        raise NotImplementedError("Method not implemented")
