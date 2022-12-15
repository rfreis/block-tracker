from django.contrib import admin

from rate.models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    model = Rate
    search_fields = [
        "asset_name",
    ]
    list_display = [
        "amount_usd",
        "asset_name",
        "interval",
        "time",
    ]
    list_filter = [
        "interval",
        "time",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
