from protocol.constants import ProtocolType


class FakeClass:
    def validate_address(self, address):
        return not address.startswith("fa")

    def validate_public_key(self, public_key):
        return not public_key.startswith("f")


class Protocol:
    protocols = {
        ProtocolType.BITCOIN: FakeClass,
    }

    def __new__(cls, protocol_key):
        ProtocolClass = cls.protocols[protocol_key]
        return ProtocolClass()
