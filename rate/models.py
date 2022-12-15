from django.db import models

from rate.constants import RateInterval


class Rate(models.Model):
    asset_name = models.CharField(max_length=255)
    amount_usd = models.CharField(max_length=255)
    interval = models.IntegerField(choices=RateInterval.choices)
    time = models.DateTimeField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.amount_usd} USD/{self.asset_name}"
