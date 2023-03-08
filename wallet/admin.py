from django.contrib import admin

from wallet.models import Address, ExtendedPublicKey, UserWallet


@admin.register(ExtendedPublicKey)
class ExtendedPublicKeyAdmin(admin.ModelAdmin):
    model = ExtendedPublicKey
    search_fields = [
        "hash",
    ]
    list_display = [
        "id",
        "hash",
        "protocol_type",
    ]
    list_filter = [
        "protocol_type",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    search_fields = [
        "hash",
    ]
    list_display = [
        "id",
        "hash",
        "is_change",
        "index",
        "extended_public_key",
        "protocol_type",
    ]
    list_filter = [
        "protocol_type",
        "is_change",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    model = UserWallet
    search_fields = [
        "label",
    ]
    list_display = [
        "id",
        "user",
        "wallet_type",
        "extended_public_key",
        "address",
        "label",
    ]

    def has_change_permission(self, *args, **kwargs):
        return False
