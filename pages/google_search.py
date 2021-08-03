"""
The GoogleSearchPage class is the page object for Google's search page.
"""

# pip installed

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class GoogleSearchPage:

    # Initializer

    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:

        URL = "https://www.google.com"

        self.driver: WebDriver = driver
        self.wait: WebDriverWait = wait

        self.driver.get(URL)

    # Page Methods

    def enter_search_key(self, searchKey: str) -> None:
        """
        Enter the specified search key into main search input and press RETURN
        """

        MAIN_SEARCH_INPUT = (By.CSS_SELECTOR, ".gLFyf.gsfi"
                             )  # class="gLFyf gsfi"

        self.driver.find_element(*MAIN_SEARCH_INPUT).send_keys(
            searchKey, Keys.RETURN)

    def page_title(self) -> str:
        """Return the Web page's page title"""

        return self.driver.title
