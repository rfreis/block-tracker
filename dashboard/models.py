from django.db import models

from accounts.models import User


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name="user_asset", on_delete=models.CASCADE)
    date = models.DateField()
    balance = models.JSONField(default=dict)

    class Meta:
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="user_balance_unique",
            ),
        ]
