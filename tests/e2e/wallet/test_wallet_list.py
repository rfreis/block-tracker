import pytest

from tests.e2e.pages.wallet_list import WalletListPage


def test_wallet_not_logged_user(browser, live_server):
    browser.get("/wallet/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/wallet/" in browser.current_url


def test_wallet_empty(browser_user_one, live_server):
    browser_user_one.get("/wallet/", live_server)
    page = WalletListPage(browser_user_one)

    assert browser_user_one.title == "Wallets - Block Tracker"

    main_row = page.table_body_rows[0]
    assert main_row.text == "No Wallets were found."


@pytest.mark.usefixtures("single_bitcoin_address_one", "xpublic_key_bitcoin_one")
def test_wallet_no_user_wallet(browser_user_one, live_server):
    browser_user_one.get("/wallet/", live_server)
    page = WalletListPage(browser_user_one)

    assert browser_user_one.title == "Wallets - Block Tracker"

    main_row = page.table_body_rows[0]
    assert main_row.text == "No Wallets were found."


@pytest.mark.usefixtures(
    "user_wallet_single_bitcoin_address_one", "user_wallet_bitcoin_xpub_one"
)
def test_wallet(browser_user_one, live_server):
    browser_user_one.get("/wallet/", live_server)
    page = WalletListPage(browser_user_one)

    assert browser_user_one.title == "Wallets - Block Tracker"

    rows = page.table_body_rows
    assert len(rows) == 2

    headers = page.table_headers
    assert len(headers) == 3
    assert headers[0].text == "Protocol"
    assert headers[1].text == "Label"
    assert headers[2].text == "Type"

    row_1 = rows[0]
    columns_row_1 = page.get_row_columns(row_1)
    assert columns_row_1[0].text == "Bitcoin"
    assert columns_row_1[1].text == "Bitcoin Mainnet Single Address"
    assert columns_row_1[2].text == "Address"
    row_2 = rows[1]
    columns_row_2 = page.get_row_columns(row_2)
    assert columns_row_2[0].text == "Bitcoin"
    assert columns_row_2[1].text == "Bitcoin Mainnet Wallet from XPub"
    assert columns_row_2[2].text == "Extended Public Key"

    assert page.create_wallet_link.is_displayed() == True
