from django.db import models

from app.contrib.models import TimeStampedModel
from accounts.models import User
from protocol.constants import ProtocolType
from wallet.constants import WalletType


class ExtendedPublicKey(models.Model):
    hash = models.CharField(max_length=255)
    protocol_type = models.IntegerField(choices=ProtocolType.choices)
    balance = models.JSONField(default=dict)
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["hash", "protocol_type"],
                name="extended_public_key_unique",
            ),
        ]

    def __str__(self):
        return self.hash


class Address(models.Model):
    extended_public_key = models.ForeignKey(
        ExtendedPublicKey,
        related_name="address",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    protocol_type = models.IntegerField(choices=ProtocolType.choices)
    balance = models.JSONField(default=dict)
    hash = models.CharField(max_length=255, db_index=True)
    is_change = models.BooleanField(default=False)
    index = models.IntegerField(null=True, blank=True)
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["hash", "protocol_type"],
                name="address_unique",
            ),
        ]

    def __str__(self):
        return self.hash


class UserWallet(TimeStampedModel):
    user = models.ForeignKey(User, related_name="user_wallet", on_delete=models.PROTECT)
    extended_public_key = models.ForeignKey(
        ExtendedPublicKey,
        related_name="user_wallet",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    address = models.ForeignKey(
        Address,
        related_name="user_wallet",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    label = models.CharField(max_length=255, null=True, blank=True)
    wallet_type = models.IntegerField(choices=WalletType.choices)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(
                        wallet_type=WalletType.ADDRESS,
                        address__isnull=False,
                        extended_public_key__isnull=True,
                    )
                    | models.Q(
                        wallet_type=WalletType.EXTENDED_PUBLIC_KEY,
                        address__isnull=True,
                        extended_public_key__isnull=False,
                    )
                ),
                name="user_wallet_wallet_type",
            ),
            models.UniqueConstraint(
                fields=["user", "address"],
                name="user_wallet_address_unique",
                condition=models.Q(wallet_type=WalletType.ADDRESS),
            ),
            models.UniqueConstraint(
                fields=["user", "extended_public_key"],
                name="user_wallet_extended_public_key_unique",
                condition=models.Q(wallet_type=WalletType.EXTENDED_PUBLIC_KEY),
            ),
        ]

    @property
    def content_type(self):
        if self.wallet_type == WalletType.ADDRESS:
            return self.address
        if self.wallet_type == WalletType.EXTENDED_PUBLIC_KEY:
            return self.extended_public_key
        return None
