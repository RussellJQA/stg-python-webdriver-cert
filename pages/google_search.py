"""
This module contains GoogleSearchPage, the page object for Google's search page
"""

# pip installed

from selenium.webdriver.common.by import By


class GoogleSearchPage:

    # URL

    URL = "https://www.google.com"

    # Element Locators

    MAIN_SEARCH_INPUT = (By.CSS_SELECTOR, ".gLFyf.gsfi")  # class="gLFyf gsfi"
    MAIN_SEARCH_BUTTON = (By.NAME, "btnK")

    # Initializer

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Page Methods

    def display(self):
        self.driver.get(self.URL)

    def page_title(self) -> str:
        return self.driver.title