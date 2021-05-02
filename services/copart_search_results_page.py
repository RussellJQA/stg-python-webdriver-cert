"""
This module contains CopartSearchResultsPage, a class implementing functionality
for the Copart.com home page's search results
"""

# pip installed

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Custom imports

from services.selenium_expected_conditions import none_of


class CopartSearchResultsPage:

    # Element Locators

    # Elements for selecting or displaying the number of search results shown per page:
    #   1. The "Show {20/50/100} entries" selector
    NUM_ENTRIES_SELECTOR = (By.NAME, "serverSideDataTable_length")
    #   2. The "Showing {X} to {Y} of {Z} entries" indicator above the search results table
    #       (there's a similar indicator below the search results table)
    ENTRIES_SHOWN_INDICATOR = (By.ID, "serverSideDataTable_info")

    # Initializer

    def __init__(self, copart_home):
        self.driver = copart_home.driver
        self.wait = copart_home.wait

    def wait_for_results_per_page_to_change(self, entries_shown_on_the_page):

        # Allow a TimeOutException for the WebDriverWait(),
        #   in case the number of entries displayed on the page doesn't change.
        # For example: If there are exactly 20 total entries,
        #   then changing from "Show 20 entries" (per page) to "Show 100 entries"
        #   won't change the number displayed from "Showing 1 to 20 of 20 entries"
        try:
            self.wait.until(
                none_of(
                    EC.text_to_be_present_in_element(
                        self.ENTRIES_SHOWN_INDICATOR,
                        entries_shown_on_the_page)))

        except TimeoutException:
            print(
                "\nWarning: Timed out waiting for the number of entries shown on the page "
                +
                f"to change from '{entries_shown_on_the_page}', which isn't necessarily a problem."
            )

    def get_entries_shown_on_the_page(self):
        # Wait for the indicator to show how many entries are displayed on the page
        self.wait.until(
            EC.text_to_be_present_in_element(self.ENTRIES_SHOWN_INDICATOR,
                                             "entries"))
        entries_shown_indicator = self.driver.find_element(
            *self.ENTRIES_SHOWN_INDICATOR)

        # Get the number of entries that are displayed on the page
        return entries_shown_indicator.text

    def set_results_per_page(self, entries_per_page: int):
        """Select the number of entries to include in the page's results table"""

        select = self.wait.until(
            EC.presence_of_element_located(self.NUM_ENTRIES_SELECTOR))

        entries_shown_on_the_page = self.get_entries_shown_on_the_page()

        # Change the selected number of entries to display per page
        Select(select).select_by_visible_text(str(entries_per_page))

        self.wait_for_results_per_page_to_change(entries_shown_on_the_page)

    def wait_for_search_results_to_be_loaded(self):
        """Wait for search results to be loaded."""

        # Adapted from set_results_per_page()
        self.wait.until(
            EC.presence_of_element_located(self.NUM_ENTRIES_SELECTOR))
        self.wait.until(
            EC.text_to_be_present_in_element(self.ENTRIES_SHOWN_INDICATOR,
                                             "entries"))