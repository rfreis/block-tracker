from protocol.bitcoin import Bitcoin, BitcoinTestnet
from protocol.constants import ProtocolType


class Protocol:
    protocols = {
        ProtocolType.BITCOIN: Bitcoin,
        ProtocolType.BITCOIN_TESTNET: BitcoinTestnet,
    }

    def __new__(cls, protocol_key):
        ProtocolClass = cls.protocols[protocol_key]
        return ProtocolClass(protocol_type=protocol_key)
