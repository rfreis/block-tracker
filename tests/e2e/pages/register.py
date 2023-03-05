from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class RegisterPage(BasePage):
    @property
    def input_first_name(self):
        return self.browser.find_element(By.ID, "id_first_name")

    @property
    def input_last_name(self):
        return self.browser.find_element(By.ID, "id_last_name")

    @property
    def input_email(self):
        return self.browser.find_element(By.ID, "id_email")

    @property
    def input_password1(self):
        return self.browser.find_element(By.ID, "id_password1")

    @property
    def input_password2(self):
        return self.browser.find_element(By.ID, "id_password2")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#register-form button[type=submit]"
        )

    @property
    def error_list(self):
        return self.browser.find_element(By.CSS_SELECTOR, "ul.errorlist")

    @property
    def errors_list(self):
        return self.browser.find_elements(By.CSS_SELECTOR, "ul.errorlist")

    @property
    def text_email(self):
        return self.browser.find_element(By.CSS_SELECTOR, "p.text-email")
