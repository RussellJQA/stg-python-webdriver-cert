"""
This module contains CopartHomePage, the page object for Copart's home page
"""

# Imports Python 3.9+'s ability to use "tuple[str, str]" below for 3.7 <= Python < 3.9,
# rather than having to use "from typing import Tuple" with "Tuple[str, str]"
from __future__ import annotations

# pip installed

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Custom imports

from services.selenium_expected_conditions import wait_for_element_to_be_clickable


class CopartHomePage:

    # URL
    URL = "https://www.copart.com"

    # Element Locators

    MAIN_SEARCH_INPUT = (By.ID, "input-search")
    MAIN_SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), 'Search')]")

    # Elements on the page's "Trending" tab
    MOST_POPULAR_ITEMS = (
        By.XPATH, "//div/h3[contains(text(), 'Most Popular Items')]/..")
    MAKES_MODELS = (
        By.XPATH,
        "./div/div/div/h4[contains(text(), 'Makes/Models')]/../../..")
    MAKE_MODEL_LINK = (By.XPATH, "./div/div/ul/li/a")
    MAKE_MODEL_MORE_LINK = (By.XPATH, "./div/div/ul/li/a[text()='More...']")

    # Elements in the search results table
    TBODY = (By.XPATH, "//table[@id='serverSideDataTable']/tbody")

    # Initializer

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Static (Class Level) Methods

    @staticmethod
    def td_span_locator(span_type: str,
                        span_match_criteria=None) -> tuple[str, str]:
        if span_match_criteria:
            return (
                By.XPATH,
                f"//table[@id='serverSideDataTable']/tbody/tr/td/span[@data-uname='lotsearchLot{span_type}' and {span_match_criteria}]"
            )
        else:
            return (
                By.XPATH,
                f"//table[@id='serverSideDataTable']/tbody/tr/td/span[@data-uname='lotsearchLot{span_type}']"
            )

    # Page (Object Level) Methods

    def display(self):
        self.driver.get(self.URL)

    def select_tab_link(self, tab_name: str):

        # Create an element locator for the tab's link, find it, and click it
        tab_link = (By.XPATH, f"//a[text()='{tab_name}']")
        self.wait.until(EC.element_to_be_clickable(tab_link)).click()

        # Wait for the tab's link to be active
        tab_link_active = (By.XPATH,
                           f"//li[@class='active']/a[text()='{tab_name}']")

        self.wait.until(EC.element_to_be_clickable(tab_link_active))

    def get_most_popular_items(self) -> list:

        # Click the "Trending" tab to make the "Most Popular Items" heading visible
        self.select_tab_link("Trending")

        #  Locate the <div> containing the "Most Popular Items" h3 heading
        div_most_popular = self.driver.find_element(*self.MOST_POPULAR_ITEMS)

        # Within div_most_popular, locate the <div> containing the "Makes/Models" h4 heading
        div_makes_models = div_most_popular.find_element(*self.MAKES_MODELS)

        # Wait for the Makes/Models "More..." link to be clickable
        wait_for_element_to_be_clickable(div_makes_models,
                                         self.MAKE_MODEL_MORE_LINK)

        # Within div_makes_models, locate the list items' links
        make_model_links = div_makes_models.find_elements(
            *self.MAKE_MODEL_LINK)

        most_popular_items = [[link.text,
                               link.get_attribute('href')]
                              for link in make_model_links
                              if link.text != "More..."]

        return most_popular_items

    def search_results_contain(self, span_type: str, span_match_criteria: str):
        tbody = self.wait.until(EC.presence_of_element_located(self.TBODY))

        span_locator = CopartHomePage.td_span_locator(span_type.lower(),
                                                      span_match_criteria)
        self.wait.until(EC.presence_of_element_located((span_locator)))
        spans = self.driver.find_elements(*span_locator)