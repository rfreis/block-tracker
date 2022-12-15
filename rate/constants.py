from django.db.models import IntegerChoices


class RateInterval(IntegerChoices):
    DAILY = 1, "Daily"
    FIVE_MIN = 2, "5 min"
