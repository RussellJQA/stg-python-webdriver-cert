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
        url = "https://www.google.com"

        self.driver: WebDriver = driver
        self.wait: WebDriverWait = wait

        self.driver.get(url)

    # Page Methods

    def enter_search_key(self, search_key: str) -> None:
        """
        Enter the specified search key into main search input and press RETURN
        """

        main_search_input = (By.CSS_SELECTOR, ".gLFyf.gsfi"
                             )  # class="gLFyf gsfi"

        self.driver.find_element(*main_search_input).send_keys(
            search_key, Keys.RETURN)

    def page_title(self) -> str:
        """Return the Web page's page title"""

        return self.driver.title
