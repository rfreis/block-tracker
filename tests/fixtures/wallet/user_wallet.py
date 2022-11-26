import pytest

from wallet.constants import WalletType
from wallet.models import UserWallet


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_single_bitcoin_address_one(user_one, single_bitcoin_address_one):
    user_wallet = UserWallet.objects.create(
        user=user_one,
        address=single_bitcoin_address_one,
        label="Bitcoin Mainnet Single Address",
        wallet_type=WalletType.ADDRESS,
    )

    yield user_wallet

    user_wallet.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_bitcoin_xpub_one(user_one, xpublic_key_bitcoin_one):
    user_wallet = UserWallet.objects.create(
        user=user_one,
        extended_public_key=xpublic_key_bitcoin_one,
        label="Bitcoin Mainnet Wallet from XPub",
        wallet_type=WalletType.EXTENDED_PUBLIC_KEY,
    )

    yield user_wallet

    user_wallet.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_bitcoin_xpub_two(user_one, xpublic_key_bitcoin_two):
    user_wallet = UserWallet.objects.create(
        user=user_one,
        extended_public_key=xpublic_key_bitcoin_two,
        label="Bitcoin Mainnet Wallet from XPub two",
        wallet_type=WalletType.EXTENDED_PUBLIC_KEY,
    )

    yield user_wallet

    user_wallet.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_wallet_bitcoin_xpub_one_user_two(user_two, xpublic_key_bitcoin_one):
    user_wallet = UserWallet.objects.create(
        user=user_two,
        extended_public_key=xpublic_key_bitcoin_one,
        label="Bitcoin Mainnet Wallet from XPub",
        wallet_type=WalletType.EXTENDED_PUBLIC_KEY,
    )

    yield user_wallet

    user_wallet.delete()
