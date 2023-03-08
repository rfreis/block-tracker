from django.db.models.signals import post_save
from django.dispatch import receiver

from transaction.tasks import new_address, new_extended_public_key
from wallet.models import Address, ExtendedPublicKey
from wallet.utils import derive_addresses_from_extended_public_key


@receiver(post_save, sender=Address)
def sync_transactions(sender, instance, update_fields, created, *args, **kwargs):
    if created:
        if not instance.extended_public_key:
            new_address.delay(instance.id)


@receiver(post_save, sender=ExtendedPublicKey)
def derive_addresses_and_sync_transactions(
    sender, instance, update_fields, created, *args, **kwargs
):
    if created:
        derive_addresses_from_extended_public_key(instance)
        new_extended_public_key.delay(instance.id)
