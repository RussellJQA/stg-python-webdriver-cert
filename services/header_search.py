"""
This module contains HeaderSearch, which can do the main/header search on both Google.com and Copart.com
"""
# pip installed

from selenium.webdriver.support import expected_conditions as EC


class HeaderSearch:

    # Initializer

    def __init__(self, search_page):
        self.driver = search_page.driver
        self.wait = search_page.wait
        self.MAIN_SEARCH_INPUT = search_page.MAIN_SEARCH_INPUT
        self.MAIN_SEARCH_BUTTON = search_page.MAIN_SEARCH_BUTTON

    def search(self, query: str):
        search_input = self.driver.find_element(*self.MAIN_SEARCH_INPUT)
        search_input.send_keys(query)

        # Click the search button, rather than sending Keys.RETURN,
        # because Keys.RETURN cluttered the search page with auto-suggestions.
        search_button = self.wait.until(
            EC.element_to_be_clickable(self.MAIN_SEARCH_BUTTON))
        search_button.click()
