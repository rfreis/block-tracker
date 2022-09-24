import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.e2e.pages.login import LoginPage


def test_login_page(browser, live_server, default_password, user_one):
    browser.get("/accounts/login/", live_server)
    page = LoginPage(browser)

    assert browser.title == "Login - Block Tracker"

    page.input_username.send_keys(user_one.username)
    page.input_password.send_keys(default_password)
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/dashboard/"))


def test_login_invalid_data(browser, live_server, user_one):
    browser.get("/accounts/login/", live_server)
    page = LoginPage(browser)

    page.input_username.send_keys(user_one.username)
    page.input_password.send_keys("wrong_password")
    page.submit_button.click()

    page.wait_for(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))

    danger_alerts = page.danger_alerts
    assert len(danger_alerts) == 1
    assert (
        danger_alerts[0].text
        == "Please enter a correct username and password. Note that both fields may be case-sensitive."
    )
