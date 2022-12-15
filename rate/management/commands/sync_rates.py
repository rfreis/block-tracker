from django.core.management import BaseCommand, CommandError

from rate.utils import sync_rates


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_rates()
