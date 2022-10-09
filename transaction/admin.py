from django.contrib import admin

from transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    search_fields = [
        "tx_id",
    ]
    list_display = [
        "id",
        "tx_id",
        "amount_usd",
        "amount_coin",
        "block_id",
        "is_confirmed",
    ]
    list_filter = [
        "address__protocol_type",
        "is_confirmed",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
