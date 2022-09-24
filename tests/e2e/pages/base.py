from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def wait_for(self, condition):
        return WebDriverWait(self.browser, 30).until(condition)

    def get_by_selector(self, element, selector):
        return element.find_element(By.CSS_SELECTOR, selector)
