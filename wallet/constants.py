from django.db.models import IntegerChoices


class WalletType(IntegerChoices):
    EXTENDED_PUBLIC_KEY = 1, "Extended Public Key"
    ADDRESS = 2, "Address"
