"""
This module contains CopartFilters, a class implementing functionality for
the filters on the left hand side of the Copart.com home page
"""

# Import Python 3.9+'s ability to use "tuple[str, str]" below for 3.7 <= Python < 3.9,
# rather than having to use "from typing import Tuple" with "Tuple[str, str]"
from __future__ import annotations

import datetime

# pip installed

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Custom imports

from services.copart_search_results_page import CopartSearchResultsPage
from services.header_search import HeaderSearch
from services.selenium_expected_conditions import (
    wait_for_element_to_be_clickable)


class CopartFilters:

    # Element locators

    SPAN_FILTER_ICON = (By.CLASS_NAME, "filter-icon")
    FILTER_SECTION_SEARCH_INPUT = (By.XPATH, "./div/form/div/input")

    # Initializer

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Static (Class Level) Methods

    @staticmethod
    def get_filter_section_expand_link_locator(
            filter_name: str) -> tuple[str, str]:
        return (
            By.XPATH,
            f"//li[@class='list-group-item']/h4/a[text()='{filter_name.title()}']"
        )

    @staticmethod
    def get_filter_checkbox_locator(filter_value: str) -> list[str, str]:
        return (
            By.XPATH,
            f"//div[@class='checkbox']//label//input/..//abbr[contains(text(), '{filter_value.title()}')]/..//input"
        )

    def expand_filter_section(self, filter_name):
        # Click "Filter Options" icon to open left-side "Filter Options" panel
        filter_options_icon = self.wait.until(
            EC.element_to_be_clickable(self.SPAN_FILTER_ICON))
        filter_options_icon.click()

        # Expand the filter section, by clicking its expand icon link
        filter_section_expand_link_locator = self.get_filter_section_expand_link_locator(
            filter_name)
        filter_section_expand_link = self.wait.until(
            EC.element_to_be_clickable(filter_section_expand_link_locator))
        filter_section_expand_link.click()

        self.filter_section = filter_section_expand_link.find_element(
            By.XPATH, "../..")  # Find filter_section_expand_link's grandparent

    def search_filter_section(self, filter_value):
        # Within the filter section, wait for the search input to be clickable,
        # and enter into it the filter value to search for, followed by a <CR>
        wait_for_element_to_be_clickable(self.filter_section,
                                         self.FILTER_SECTION_SEARCH_INPUT)
        self.filter_section.find_element(
            *self.FILTER_SECTION_SEARCH_INPUT).send_keys(filter_value +
                                                         Keys.RETURN)

    def click_filter_checkboxes(self, filter_name, filter_value):

        filter_checkbox_locator = CopartFilters.get_filter_checkbox_locator(
            filter_value)

        # Wait for at least 1 filter checkbox to be clickable
        wait_for_element_to_be_clickable(self.filter_section,
                                         filter_checkbox_locator)

        filter_checkboxes = self.filter_section.find_elements(
            *filter_checkbox_locator)

        for filter_checkbox in filter_checkboxes:
            filter_checkbox.click()

    def do_filtered_search(self, driver, wait, search_page, query, filter_name,
                           filter_value):

        HeaderSearch(search_page).search(query)

        self.expand_filter_section(filter_name)
        self.search_filter_section(filter_value)

        # Within the filter section, click the appropriate search checkboxes
        self.click_filter_checkboxes(query, filter_value)

        # Wait to allow search results per page to change
        copart_search_results_page = CopartSearchResultsPage(search_page)
        entries_shown_on_the_page = copart_search_results_page.get_entries_shown_on_the_page(
        )
        copart_search_results_page.wait_for_results_per_page_to_change(
            entries_shown_on_the_page)