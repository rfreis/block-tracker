from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class PasswordChangePage(BasePage):
    @property
    def input_old_password(self):
        return self.browser.find_element(By.ID, "id_old_password")

    @property
    def input_new_password1(self):
        return self.browser.find_element(By.ID, "id_new_password1")

    @property
    def input_new_password2(self):
        return self.browser.find_element(By.ID, "id_new_password2")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#change-password-form button[type=submit]"
        )

    @property
    def error_list(self):
        return self.browser.find_element(By.CSS_SELECTOR, "ul.errorlist")
