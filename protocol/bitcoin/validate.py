class BitcoinValidateMixin:
    @staticmethod
    def _data_from_leading_symbols(address, settings):
        for semantic, data in settings.items():
            for leading_symbol in data.get("leading_symbols", []):
                if str(address).startswith(leading_symbol):
                    return semantic, data
        return None, None

    @classmethod
    def _validate(cls, value, settings):
        semantic, data = cls._data_from_leading_symbols(value, settings)
        if not data:
            return False, None
        validate_function = data["validate_function"]
        return validate_function(value, **data.get("kwargs", {})), semantic

    @classmethod
    def validate_address(cls, address):
        return cls._validate(address, cls.addresses)

    @classmethod
    def validate_xpublic_key(cls, xpublic_key):
        return cls._validate(xpublic_key, cls.extended_pubkeys)
