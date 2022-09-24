import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from django.core import mail

from tests.e2e.pages.password_reset import PasswordResetPage, PasswordResetConfirmPage


@pytest.mark.usefixtures("django_db_reset_sequences")
def test_password_reset_page(mocker, browser, live_server, user_one):
    mocker.patch(
        "accounts.views.PasswordResetView.token_generator.make_token",
        return_value="random_token",
    )
    browser.get("/accounts/password_reset/", live_server)
    page = PasswordResetPage(browser)

    assert browser.title == "Password reset - Block Tracker"

    page.input_email.send_keys(user_one.email)
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/accounts/password_reset/done/"))

    assert len(mail.outbox) == 1
    sent_email = mail.outbox[0]
    clean_live_server_str = str(live_server).replace("http://", "")
    link_reset_url = f"{live_server}/accounts/reset/MQ/random_token/"
    expected_body_txt = (
        "\nYou're receiving this email because you requested a password reset for your user account"
        f" at {clean_live_server_str}.\n\n"
        "Please go to the following page and choose a new password:\n\n"
        f"{link_reset_url}\n\n"
        f"Your username, in case you’ve forgotten: {user_one.username}\n\n"
        "Thanks for using our site!\n\n"
        f"The {clean_live_server_str} team\n\n\n"
    )
    expected_body_html = (
        "\n<p>You're receiving this email because you requested a password reset for your user account "
        f'at <a href="{live_server}">{clean_live_server_str}</a>.</p>\n\n'
        "<p>Please go to the following page and choose a new password:</p>\n\n"
        f'<ul>\n<li><a href="{link_reset_url}">{link_reset_url}</a></li>\n</ul>\n\n<p>'
        f"Your username, in case you’ve forgotten: <strong>{user_one.username}</strong></p>\n\n"
        "<p>Thanks for using our site!</p>\n\n"
        f"<p>The {clean_live_server_str} team</p>\n\n\n"
    )

    assert sent_email.to == [user_one.email]
    assert sent_email.subject == f"Password reset on {clean_live_server_str}"
    assert sent_email.from_email == "test_sender@example.com"
    assert sent_email.body == expected_body_txt
    assert sent_email.alternatives[0][1] == "text/html"
    assert sent_email.alternatives[0][0] == expected_body_html


def test_password_reset_page_invalid_username(browser, live_server):
    browser.get("/accounts/password_reset/", live_server)
    page = PasswordResetPage(browser)

    assert browser.title == "Password reset - Block Tracker"

    page.input_email.send_keys("wrong@email.com")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/accounts/password_reset/done/"))

    assert len(mail.outbox) == 0


@pytest.mark.usefixtures("django_db_reset_sequences")
def test_password_reset_confirm_page(mocker, browser, live_server, user_one):
    mocker.patch(
        "accounts.views.PasswordResetConfirmView.token_generator.check_token",
        return_value=True,
    )
    browser.get("/accounts/reset/MQ/random_token/", live_server)
    page = PasswordResetConfirmPage(browser)

    assert browser.title == "Enter new password - Block Tracker"

    page.input_new_password1.send_keys("new_password")
    page.input_new_password2.send_keys("new_password")
    page.submit_button.click()

    page.wait_for(EC.url_to_be(f"{live_server}/accounts/reset/done/"))

    user_one.refresh_from_db()
    assert user_one.check_password("new_password") == True
