from selenium.webdriver.common.by import By

from tests.e2e.pages.base import BasePage


class DashboardPage(BasePage):
    @property
    def card_assets(self):
        return self.browser.find_element(By.CSS_SELECTOR, "div.dashboard-assets")

    @property
    def card_performance(self):
        return self.browser.find_element(By.CSS_SELECTOR, "div.dashboard-performance")

    @property
    def card_wallets(self):
        return self.browser.find_element(By.CSS_SELECTOR, "div.dashboard-wallets")

    @property
    def card_transactions(self):
        return self.browser.find_element(By.CSS_SELECTOR, "div.dashboard-transactions")

    @property
    def card_last_transactions(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "div.dashboard-last-transactions"
        )

    @property
    def table_transactions(self):
        return self.card_last_transactions.find_element(
            By.CSS_SELECTOR, "table#transaction_list"
        )

    @property
    def table_transactions_headers(self):
        return self.table_transactions.find_elements(By.CSS_SELECTOR, "thead tr th")

    @property
    def table_transactions_body_rows(self):
        return self.table_transactions.find_elements(By.CSS_SELECTOR, "tbody tr")
