from django.db.models import IntegerChoices


class ProtocolType(IntegerChoices):
    BITCOIN = 1, "Bitcoin"


class CoinType(IntegerChoices):
    BTC = 1, "BTC"
