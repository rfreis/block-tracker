import pytest
from freezegun import freeze_time

from tests.e2e.pages.dashboard_page import DashboardPage


def test_dashboard_not_logged_user(browser, live_server):
    browser.get("/dashboard/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/dashboard/" in browser.current_url


@freeze_time("2022-12-31 12:00:00")
@pytest.mark.usefixtures(
    "rate_bitcoin_history",
    "user_balance_history",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one_user_two",
    "transaction_derived_bitcoin_address_three",
)
def test_dashboard(
    browser_user_one,
    live_server,
    client_user_one,
    transaction_single_bitcoin_address_one,
):
    browser_user_one.get("/dashboard/", live_server)
    page = DashboardPage(browser_user_one)

    assert browser_user_one.title == "Dashboard - Block Tracker"

    assert page.card_assets.text == "ASSETS\n$8,302"
    assert page.card_performance.text == "PERFORMANCE VS LAST MONTH\n$81 (1.0%)"
    assert page.card_wallets.text == "WALLETS\n1"
    assert page.card_transactions.text == "TRANSACTIONS\n1"

    rows = page.table_transactions_body_rows
    assert len(rows) == 1

    headers = page.table_transactions_headers
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
    assert columns_row_1[1].text == transaction_single_bitcoin_address_one.tx_id
    assert columns_row_1[2].text == "0.00288733 BTC"
    assert columns_row_1[3].text == "$ 25.73"
    assert columns_row_1[4].text == "Yes"
    assert columns_row_1[5].text == "13/02/2018"

    res = client_user_one.get("/dashboard/")
    context = res.context[0]
    expected_monthly_amount_usd = [
        {
            "date": "01/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "02/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "03/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "04/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "05/2022",
            "total_amount_usd": "15870.470362583475",
            "amount_usd_by_asset": {"BTC": "15870.470362583475"},
            "balance": {"BTC": "0.5"},
        },
        {
            "date": "06/2022",
            "total_amount_usd": "10054.2647364448910",
            "amount_usd_by_asset": {"BTC": "10054.2647364448910"},
            "balance": {"BTC": "0.5"},
        },
        {
            "date": "07/2022",
            "total_amount_usd": "11826.7297747153990",
            "amount_usd_by_asset": {"BTC": "11826.7297747153990"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "08/2022",
            "total_amount_usd": "9902.675349429020",
            "amount_usd_by_asset": {"BTC": "9902.675349429020"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "09/2022",
            "total_amount_usd": "9781.8825808884520",
            "amount_usd_by_asset": {"BTC": "9781.8825808884520"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "10/2022",
            "total_amount_usd": "10311.9357485204730",
            "amount_usd_by_asset": {"BTC": "10311.9357485204730"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "11/2022",
            "total_amount_usd": "8220.9899892095565",
            "amount_usd_by_asset": {"BTC": "8220.9899892095565"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "12/2022",
            "total_amount_usd": "8302.0102601866965",
            "amount_usd_by_asset": {"BTC": "8302.0102601866965"},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
    ]
    assert context["monthly_amount_usd"] == expected_monthly_amount_usd
    expected_asset_dominance = [
        {
            "asset_name": "BTC",
            "amount_usd": "8302.0102601866965",
            "background_color": "#4e73df",
            "background_color_hover": "#2e59d9",
        }
    ]
    assert context["asset_dominance"] == expected_asset_dominance


@freeze_time("2022-12-31 12:00:00")
@pytest.mark.usefixtures(
    "user_balance_history",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one_user_two",
    "transaction_derived_bitcoin_address_three",
)
def test_dashboard_without_rates(
    browser_user_one,
    live_server,
    client_user_one,
    transaction_single_bitcoin_address_one,
):
    browser_user_one.get("/dashboard/", live_server)
    page = DashboardPage(browser_user_one)

    assert browser_user_one.title == "Dashboard - Block Tracker"

    assert page.card_assets.text == "ASSETS\n$0"
    assert page.card_performance.text == "PERFORMANCE VS LAST MONTH\n$0 (0.0%)"
    assert page.card_wallets.text == "WALLETS\n1"
    assert page.card_transactions.text == "TRANSACTIONS\n1"

    res = client_user_one.get("/dashboard/")
    context = res.context[0]
    expected_monthly_amount_usd = [
        {
            "date": "01/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "02/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "03/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "04/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {},
        },
        {
            "date": "05/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5"},
        },
        {
            "date": "06/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5"},
        },
        {
            "date": "07/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "08/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "09/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "10/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "11/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
        {
            "date": "12/2022",
            "total_amount_usd": "0",
            "amount_usd_by_asset": {},
            "balance": {"BTC": "0.5", "BTCTEST": "0.2"},
        },
    ]
    assert context["monthly_amount_usd"] == expected_monthly_amount_usd
    assert context["asset_dominance"] == []
