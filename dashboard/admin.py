from django.contrib import admin

from dashboard.models import UserBalance


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    model = UserBalance
    list_display = [
        "id",
        "user",
        "date",
    ]
    list_filter = [
        "date",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
