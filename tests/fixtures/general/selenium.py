import pytest

from selenium.webdriver import Chrome as SeleniumChrome
from selenium.webdriver.chrome.options import Options


def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


class Chrome(SeleniumChrome):
    def get(self, url, liveserver=None):
        if liveserver:
            _url = f"{liveserver.url}{url}"
            super().get(_url)
        else:
            super().get(url)


@pytest.fixture
def browser():
    chrome_options = set_chrome_options()
    driver = Chrome(options=chrome_options)

    yield driver

    driver.close()


@pytest.fixture()
def browser_user_one(browser, client_user_one, live_server):
    cookie = client_user_one.cookies["sessionid"]

    browser.get(live_server.url)
    browser.add_cookie(
        {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
    )
    browser.refresh()

    return browser
