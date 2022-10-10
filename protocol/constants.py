from django.db.models import IntegerChoices


class ProtocolType(IntegerChoices):
    BITCOIN = 1, "Bitcoin"
