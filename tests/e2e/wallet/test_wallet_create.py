import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from protocol.constants import ProtocolType
from wallet.constants import WalletType
from wallet.models import UserWallet

from tests.e2e.pages.wallet_create import WalletCreatePage


def test_wallet_create_logged_out(browser, live_server):
    browser.get("/wallet/add/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/wallet/add/" in browser.current_url


def test_wallet_create_add_address(browser_user_one, live_server, user_one):
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys("f_invalid_for_public_key_valid_for_address")
    page.input_label.send_keys("Wallet for Single Address")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/wallet/"))

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 1
    user_wallet = user_wallets.first()
    assert user_wallet.user == user_one
    assert user_wallet.public_key == None
    assert user_wallet.address.hash == "f_invalid_for_public_key_valid_for_address"
    assert user_wallet.address.protocol_type == ProtocolType.BITCOIN
    assert user_wallet.label == "Wallet for Single Address"
    assert user_wallet.wallet_type == WalletType.ADDRESS


def test_wallet_create_add_public_key(browser_user_one, live_server, user_one):
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys("valid_for_public_key_hash")
    page.input_label.send_keys("Wallet for Extended Public Key")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/wallet/"))

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 1
    user_wallet = user_wallets.first()
    assert user_wallet.user == user_one
    assert user_wallet.public_key.hash == "valid_for_public_key_hash"
    assert user_wallet.public_key.protocol_type == ProtocolType.BITCOIN
    assert user_wallet.address == None
    assert user_wallet.label == "Wallet for Extended Public Key"
    assert user_wallet.wallet_type == WalletType.PUBLIC_KEY


def test_wallet_create_invalid_hash(browser_user_one, live_server):
    browser_user_one.get("/wallet/add/", live_server)
    page = WalletCreatePage(browser_user_one)

    assert browser_user_one.title == "Add Wallet - Block Tracker"

    user_wallets = UserWallet.objects.all()
    assert user_wallets.count() == 0

    page.input_hash.send_keys("fa_invalid_for_both_hash")
    page.input_label.send_keys("Invalid Wallet")
    page.input_protocol_type.send_keys("1")
    page.submit_button.click()

    page.wait_for(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.errorlist")))

    assert "The hash is invalid for the selected protocol." in page.error_list.text
