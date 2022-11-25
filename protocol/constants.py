from django.db.models import IntegerChoices


class ProtocolType(IntegerChoices):
    BITCOIN = 1, "Bitcoin"
    BITCOIN_TESTNET = 90001, "Bitcoin (Testnet)"
