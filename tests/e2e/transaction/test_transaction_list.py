import pytest  # noqa: F401

from tests.e2e.pages.transaction_list import TransactionListPage


def test_transaction_not_logged_user(browser, live_server):
    browser.get("/transaction/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/transaction/" in browser.current_url


def test_transaction_empty(browser_user_one, live_server):
    browser_user_one.get("/transaction/", live_server)
    page = TransactionListPage(browser_user_one)

    assert browser_user_one.title == "Transactions - Block Tracker"

    main_row = page.table_body_rows[0]
    assert main_row.text == "No Transactions were found."


@pytest.mark.usefixtures(
    "transaction_single_bitcoin_address_one",
    "transaction_derived_bitcoin_address_three",
)
def test_transaction_no_user_wallet(browser_user_one, live_server):
    browser_user_one.get("/transaction/", live_server)
    page = TransactionListPage(browser_user_one)

    assert browser_user_one.title == "Transactions - Block Tracker"

    main_row = page.table_body_rows[0]
    assert main_row.text == "No Transactions were found."


@pytest.mark.usefixtures(
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_two",
)
def test_transaction(
    browser_user_one,
    live_server,
    transaction_single_bitcoin_address_one,
    transaction_derived_bitcoin_address_three,
):
    browser_user_one.get("/transaction/", live_server)
    page = TransactionListPage(browser_user_one)

    assert browser_user_one.title == "Transactions - Block Tracker"

    rows = page.table_body_rows
    assert len(rows) == 2

    headers = page.table_headers
    assert len(headers) == 6
    assert headers[0].text == "Protocol"
    assert headers[1].text == "Tx. ID"
    assert headers[2].text == "Amount Asset"
    assert headers[3].text == "Amount USD"
    assert headers[4].text == "Is Confirmed"
    assert headers[5].text == "Date"

    row_1 = rows[0]
    columns_row_1 = page.get_row_columns(row_1)
    assert columns_row_1[0].text == "Bitcoin"
    assert columns_row_1[1].text == transaction_derived_bitcoin_address_three.tx_id
    assert columns_row_1[2].text == "-0.00067396 BTC"
    assert columns_row_1[3].text == "$ 0.00"
    assert columns_row_1[4].text == "Yes"
    assert columns_row_1[5].text == "13/02/2018"
    row_2 = rows[1]
    columns_row_2 = page.get_row_columns(row_2)
    assert columns_row_2[0].text == "Bitcoin"
    assert columns_row_2[1].text == transaction_single_bitcoin_address_one.tx_id
    assert columns_row_2[2].text == "0.00288733 BTC"
    assert columns_row_2[3].text == "$ 25.73"
    assert columns_row_2[4].text == "Yes"
    assert columns_row_2[5].text == "13/02/2018"


@pytest.mark.usefixtures(
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_two",
)
def test_transaction_orphan(
    browser_user_one,
    live_server,
    transaction_single_bitcoin_address_one,
    transaction_derived_bitcoin_address_three,
):
    transaction_derived_bitcoin_address_three.is_orphan = True
    transaction_derived_bitcoin_address_three.save()

    browser_user_one.get("/transaction/", live_server)
    page = TransactionListPage(browser_user_one)

    rows = page.table_body_rows
    assert len(rows) == 1

    row_1 = rows[0]
    columns_row_1 = page.get_row_columns(row_1)
    assert columns_row_1[1].text == transaction_single_bitcoin_address_one.tx_id
