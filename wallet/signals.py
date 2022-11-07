from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import ExtendedPublicKey
from wallet.utils import derive_addresses_from_extended_public_key


@receiver(post_save, sender=ExtendedPublicKey)
def derive_addresses(sender, instance, update_fields, created, *args, **kwargs):
    if created:
        derive_addresses_from_extended_public_key(instance)
