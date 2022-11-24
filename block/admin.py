from django.contrib import admin

from block.models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    model = Block
    search_fields = [
        "block_id",
        "block_hash",
    ]
    list_display = [
        "id",
        "protocol_type",
        "block_id",
        "block_hash",
        "is_confirmed",
        "is_orphan",
        "is_confirmed",
    ]
    list_filter = [
        "protocol_type",
        "is_confirmed",
        "is_orphan",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
