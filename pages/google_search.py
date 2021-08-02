"""
This module contains GoogleSearchPage, the page object for Google's search page
"""

# pip installed

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class GoogleSearchPage:

    # Initializer

    def __init__(self, driver, wait):

        URL = "https://www.google.com"

        self.driver = driver
        self.wait = wait
        self.driver.get(URL)

    # Page Methods

    def enter_search_key(self, searchKey):
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
