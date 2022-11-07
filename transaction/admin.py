from django.contrib import admin

from transaction.models import Transaction, InputData, OutputData


class InputDataInline(admin.StackedInline):
    model = InputData
    classes = ["collapse"]


class OutputDataInline(admin.StackedInline):
    model = OutputData
    classes = ["collapse"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    search_fields = [
        "tx_id",
        "inputs__hash",
        "outputs__hash",
        "inputs__extended_public_key__hash",
        "outputs__extended_public_key__hash",
    ]
    list_display = [
        "id",
        "tx_id",
        "block_id",
        "inputs",
        "outputs",
        "is_confirmed",
        "block_time",
    ]
    list_filter = [
        "block_time",
        "is_confirmed",
    ]
    inlines = [
        InputDataInline,
        OutputDataInline,
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
