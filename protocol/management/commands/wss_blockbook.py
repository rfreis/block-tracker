from django.core.management import BaseCommand, CommandError

from protocol import Protocol, ProtocolType


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "protocol_type_attr",
            type=str,
            help="The protocol attribute from ProtocolType. (e.g. BITCOIN for ProtocolType.BITCOIN)",
        )

    def handle(self, *args, **options):
        protocol_type_attr = options["protocol_type_attr"]
        if not hasattr(ProtocolType, protocol_type_attr):
            raise CommandError("ProtocolType attr %s invalid" % protocol_type_attr)

        protocol_type = getattr(ProtocolType, protocol_type_attr)
        protocol = Protocol(protocol_type)
        protocol.wss_backend.start()
