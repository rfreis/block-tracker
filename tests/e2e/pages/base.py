from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def wait_for(self, condition):
        return WebDriverWait(self.browser, 30).until(condition)

    def get_row_columns(self, row):
        return row.find_elements(By.CSS_SELECTOR, "td")
