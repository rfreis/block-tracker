import pytest

from wallet.constants import WalletType
from wallet.models import UserWallet


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_fake_single_address_one(user_one, fake_single_address_one):
    user_wallet = UserWallet.objects.create(
        user=user_one,
        address=fake_single_address_one,
        label="Fake Wallet for Single Address",
        wallet_type=WalletType.ADDRESS,
    )
    user_wallet.save()

    yield user_wallet

    user_wallet.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_fake_derived_address_one(user_one, fake_public_key_one):
    user_wallet = UserWallet.objects.create(
        user=user_one,
        public_key=fake_public_key_one,
        label="Fake Wallet for Public Key",
        wallet_type=WalletType.PUBLIC_KEY,
    )
    user_wallet.save()

    yield user_wallet

    user_wallet.delete()
