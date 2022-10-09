from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class WalletCreatePage(BasePage):
    @property
    def input_hash(self):
        return self.browser.find_element(By.ID, "id_hash")

    @property
    def input_label(self):
        return self.browser.find_element(By.ID, "id_label")

    @property
    def input_protocol_type(self):
        return self.browser.find_element(By.ID, "id_protocol_type")

    @property
    def submit_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form#create-wallet-form button[type=submit]"
        )

    @property
    def error_list(self):
        return self.browser.find_element(By.CSS_SELECTOR, "ul.errorlist")
