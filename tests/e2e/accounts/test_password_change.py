import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.e2e.pages.password_change import PasswordChangePage


def test_password_change_page(browser_user_one, live_server, default_password):
    browser_user_one.get("/accounts/password_change/", live_server)
    page = PasswordChangePage(browser_user_one)

    assert browser_user_one.title == "Password change - Block Tracker"

    page.input_old_password.send_keys(default_password)
    page.input_new_password1.send_keys("new_password")
    page.input_new_password2.send_keys("new_password")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/accounts/password_change/done/"))


def test_password_change_invalid_password(browser_user_one, live_server):
    browser_user_one.get("/accounts/password_change/", live_server)
    page = PasswordChangePage(browser_user_one)

    assert browser_user_one.title == "Password change - Block Tracker"

    page.input_old_password.send_keys("wrong_password")
    page.input_new_password1.send_keys("new_password")
    page.input_new_password2.send_keys("new_password")
    page.submit_button.click()

    page.wait_for(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.errorlist")))

    assert (
        page.error_list.text
        == "Your old password was entered incorrectly. Please enter it again."
    )


def test_password_change_logged_out(browser, live_server):
    browser.get("/accounts/password_change/", live_server)
    assert "/accounts/login/?next=/accounts/password_change/" in browser.current_url
