from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class WalletListPage(BasePage):
    @property
    def table(self):
        return self.browser.find_element(By.ID, "wallet_list")

    @property
    def table_headers(self):
        return self.table.find_elements(By.CSS_SELECTOR, "thead tr th")

    @property
    def table_body_rows(self):
        return self.table.find_elements(By.CSS_SELECTOR, "tbody tr")

    @property
    def create_wallet_link(self):
        return self.browser.find_element(By.ID, "create_wallet_link")
