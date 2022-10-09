from django.db import models

from app.contrib.models import TimeStampedModel
from protocol import Protocol
from protocol.constants import CoinType
from wallet.models import Address


class Transaction(TimeStampedModel):
    address = models.ForeignKey(
        Address, related_name="transaction", db_index=True, on_delete=models.PROTECT
    )
    amount_usd = models.CharField(max_length=255)
    amount_coin = models.CharField(max_length=255)
    coin_type = models.IntegerField(choices=CoinType.choices)
    tx_id = models.CharField(max_length=255, db_index=True)
    block_id = models.CharField(max_length=255, null=True, blank=True)
    vin = models.CharField(max_length=255, null=True, blank=True)
    vout = models.CharField(max_length=255, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    confirmed = models.DateTimeField(null=True, blank=True)
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["address", "tx_id", "vin", "vout"],
                name="transaction_unique",
            ),
        ]

    def __str__(self):
        return self.tx_id

    @property
    def protocol(self):
        return Protocol(self.address.protocol_type)
