from uuid import uuid4

from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)

    class Meta:
        abstract = True
