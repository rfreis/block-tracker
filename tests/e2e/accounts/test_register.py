import pytest  # noqa: F401
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from accounts.models import User
from tests.e2e.pages.register import RegisterPage


def test_register_page(browser, live_server, default_password):
    queryset = User.objects.all()
    assert queryset.count() == 0

    browser.get("/accounts/register/", live_server)
    page = RegisterPage(browser)

    assert browser.title == "Register - Block Tracker"

    page.input_first_name.send_keys("User")
    page.input_last_name.send_keys("One")
    page.input_email.send_keys("user_one@email.com")
    page.input_password1.send_keys(default_password)
    page.input_password2.send_keys(default_password)
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/dashboard/"))
    assert queryset.count() == 1
    user = queryset.get(email="user_one@email.com")
    assert user.username == "user_one@email.com"
    assert user.first_name == "User"
    assert user.last_name == "One"
    assert user.is_active is True


def test_register_page_email_querystring(browser, live_server, default_password):
    queryset = User.objects.all()
    assert queryset.count() == 0

    browser.get("/accounts/register/?email=user_one@email.com", live_server)
    page = RegisterPage(browser)

    assert page.text_email.text == "Email: user_one@email.com"
    assert page.input_email.get_attribute("value") == "user_one@email.com"
    page.input_first_name.send_keys("User")
    page.input_last_name.send_keys("One")
    page.input_password1.send_keys(default_password)
    page.input_password2.send_keys(default_password)
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/dashboard/"))
    assert queryset.count() == 1
    user = queryset.get(email="user_one@email.com")
    assert user.username == "user_one@email.com"


def test_register_page_invalid_password(browser, live_server):
    browser.get("/accounts/register/", live_server)
    page = RegisterPage(browser)

    assert browser.title == "Register - Block Tracker"

    page.input_first_name.send_keys("User")
    page.input_last_name.send_keys("One")
    page.input_email.send_keys("user_one@email.com")
    page.input_password1.send_keys("default_password1")
    page.input_password2.send_keys("default_password2")
    page.submit_button.click()

    page.wait_for(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.errorlist")))

    assert page.error_list.text == "The two password fields didn’t match."
    assert User.objects.all().count() == 0
