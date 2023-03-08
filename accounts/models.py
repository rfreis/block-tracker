from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ["id"]
