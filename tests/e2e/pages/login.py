from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class LoginPage(BasePage):
    @property
    def input_username(self):
        return self.browser.find_element(By.ID, "id_username")

    @property
    def input_password(self):
        return self.browser.find_element(By.ID, "id_password")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#login-form button[type=submit]"
        )

    @property
    def danger_alerts(self):
        return self.browser.find_elements(By.CLASS_NAME, "alert-danger")
