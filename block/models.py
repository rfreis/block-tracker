from django.db import models

from app.contrib.models import TimeStampedModel
from protocol.constants import ProtocolType


class Block(TimeStampedModel):
    protocol_type = models.IntegerField(choices=ProtocolType.choices)
    block_id = models.IntegerField(db_index=True)
    block_hash = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
    is_orphan = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["protocol_type", "block_id", "block_hash"],
                name="block_unique",
            ),
        ]

    def __str__(self):
        return self.block_hash
