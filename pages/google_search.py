"""
This module contains GoogleSearchPage, the page object for Google's search page
"""

# pip installed

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class GoogleSearchPage:

    # URL
    URL = "https://www.google.com"

    # Element Locators
    MAIN_SEARCH_INPUT = (By.CSS_SELECTOR, ".gLFyf.gsfi")  # class="gLFyf gsfi"

    # Initializer

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.driver.get(self.URL)

    # Page Methods

    def enter_search_key(self, searchKey):
        self.driver.find_element(*self.MAIN_SEARCH_INPUT).send_keys(
            searchKey, Keys.RETURN)

    def page_title(self) -> str:
        return self.driver.title
