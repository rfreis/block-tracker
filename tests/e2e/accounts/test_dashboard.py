import pytest  # noqa: F401


def test_dashboard_not_logged_user(browser, live_server):
    browser.get("/dashboard/", live_server)

    assert browser.title == "Login - Block Tracker"
    assert "/accounts/login/?next=/dashboard/" in browser.current_url
