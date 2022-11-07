from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = "wallet"

    def ready(self):
        import wallet.signals
