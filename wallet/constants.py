from django.db.models import IntegerChoices


class WalletType(IntegerChoices):
    PUBLIC_KEY = 1, "Public Key"
    ADDRESS = 2, "Address"
