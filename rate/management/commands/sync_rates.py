from django.core.management import BaseCommand

from rate.utils import sync_rates


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_rates()
