from django.db import models

from app.contrib.models import TimeStampedModel
from protocol.constants import ProtocolType
from wallet.models import Address


class Transaction(TimeStampedModel):
    inputs = models.ManyToManyField(
        Address,
        related_name="inputs",
        db_index=True,
        through="InputData",
    )
    outputs = models.ManyToManyField(
        Address,
        related_name="outputs",
        db_index=True,
        through="OutputData",
    )
    protocol_type = models.IntegerField(choices=ProtocolType.choices)
    tx_id = models.CharField(max_length=255, db_index=True)
    block_id = models.IntegerField(null=True, blank=True)
    block_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["protocol_type", "tx_id"],
                name="transaction_unique",
            ),
        ]

    def __str__(self):
        return self.tx_id

    @property
    def inputs(self):
        return self.inputdata.count()

    @property
    def outputs(self):
        return self.outputdata.count()


class AbstractInputOutputData(models.Model):
    address = models.ForeignKey(
        Address,
        related_name="%(class)s",
        on_delete=models.PROTECT,
    )
    transaction = models.ForeignKey(
        Transaction,
        related_name="%(class)s",
        on_delete=models.PROTECT,
    )
    amount_usd = models.CharField(max_length=255, blank=True, null=True)
    amount_asset = models.CharField(max_length=255)
    asset_name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class InputData(AbstractInputOutputData):
    def __str__(self):
        return f"{self.amount_asset} {self.asset_name} ({self.address.hash})"


class OutputData(AbstractInputOutputData):
    def __str__(self):
        return f"{self.amount_asset} {self.asset_name} ({self.address.hash})"
