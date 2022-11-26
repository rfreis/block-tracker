import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from protocol.constants import ProtocolType
from wallet.constants import WalletType
from wallet.models import Address, UserWallet

from tests.e2e.pages.wallet_create import WalletCreatePage


def test_wallet_create_logged_out(browser, live_server):
    browser.get("/wallet/add/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/wallet/add/" in browser.current_url


@pytest.mark.enable_signals
@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
def test_wallet_create_add_address(
    mocker, browser_user_one, live_server, user_one, hash_address_p2wpkh_bitcoin_one
):
    mock_new_address = mocker.patch("wallet.signals.new_address.delay")
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys(hash_address_p2wpkh_bitcoin_one)
    page.input_label.send_keys("Wallet for Single Address")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/wallet/"))

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 1
    user_wallet = user_wallets.first()
    assert user_wallet.user == user_one
    assert user_wallet.extended_public_key == None
    assert user_wallet.address.hash == hash_address_p2wpkh_bitcoin_one
    assert user_wallet.address.protocol_type == ProtocolType.BITCOIN
    assert user_wallet.label == "Wallet for Single Address"
    assert user_wallet.wallet_type == WalletType.ADDRESS
    mock_new_address.assert_called_once_with(user_wallet.address.id)


@pytest.mark.enable_signals
@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
def test_wallet_create_add_xpublic_key(
    mocker, browser_user_one, live_server, user_one, hash_xpub_bitcoin_one
):
    mock_new_extended_public_key = mocker.patch(
        "wallet.signals.new_extended_public_key.delay"
    )
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys(hash_xpub_bitcoin_one)
    page.input_label.send_keys("Wallet for Extended Public Key")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/wallet/"))

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 1
    user_wallet = user_wallets.first()
    assert user_wallet.user == user_one
    assert user_wallet.extended_public_key.hash == hash_xpub_bitcoin_one
    assert user_wallet.extended_public_key.protocol_type == ProtocolType.BITCOIN
    assert user_wallet.address == None
    assert user_wallet.label == "Wallet for Extended Public Key"
    assert user_wallet.wallet_type == WalletType.EXTENDED_PUBLIC_KEY

    derived_addresses = Address.objects.filter(
        extended_public_key=user_wallet.extended_public_key
    )
    assert derived_addresses.count() == 84
    mock_new_extended_public_key.assert_called_once_with(
        user_wallet.extended_public_key.id
    )


def test_wallet_create_invalid_hash(browser_user_one, live_server):
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys("invalid_hash")
    page.input_label.send_keys("Invalid Wallet")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.errorlist")))

    assert "The hash is invalid for the selected protocol." in page.error_list.text
