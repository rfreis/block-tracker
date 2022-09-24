from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class PasswordResetPage(BasePage):
    @property
    def input_email(self):
        return self.browser.find_element(By.ID, "id_email")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#forgot-password-form button[type=submit]"
        )


class PasswordResetConfirmPage(BasePage):
    @property
    def input_new_password1(self):
        return self.browser.find_element(By.ID, "id_new_password1")

    @property
    def input_new_password2(self):
        return self.browser.find_element(By.ID, "id_new_password2")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#new-password-form button[type=submit]"
        )
