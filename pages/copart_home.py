"""
The CopartHomePage class is the page object for Copart.com's home page.
"""

# Import Python 3.9+'s ability to type hint lists and dictionaries directly
# into 3.7 <= Python < 3.9. Without this, you need to use
# "from typing import List" along with "List[int]", "List[str]",
# "from typing import Dict" along with "dict[str, int]", etc.

from __future__ import annotations
from typing import Optional

# pip installed

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

# Custom imports

from services.pytest_services import PytestServices
from services.selenium_screenshots import SeleniumScreenshots


class CopartHomePage:

    # Initializer

    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:

        URL = "https://www.copart.com"

        self.driver: WebDriver = driver
        self.wait: WebDriverWait = wait

        self.driver.get(URL)

    # Page Methods

    def enter_search_key(self, searchKey: str) -> None:
        """
        Enter the specified search key into main search input and press RETURN
        """

        MAIN_SEARCH_INPUT = (By.ID, "input-search")

        self.driver.find_element(*MAIN_SEARCH_INPUT).send_keys(
            searchKey, Keys.RETURN)

    def wait_for_spinner_to_come_and_go(self) -> None:
        """
        Wait for the progress spinner to be present and then become invisible
        """

        SPINNER = (By.XPATH, "//div[@id='serverSideDataTable_processing']")

        spinner = self.wait.until(EC.presence_of_element_located(SPINNER))
        self.wait.until(EC.invisibility_of_element_located(spinner))

    def get_table_text(self) -> str:
        """Return the text from the search results table WebElement"""

        TABLE = (By.XPATH, "//table[@id='serverSideDataTable']")

        return self.driver.find_element(*TABLE).text

    def click_link(self, link_text: str) -> None:
        """Click the link with the specified link text"""

        self.driver.find_element(By.LINK_TEXT, link_text).click()

    def get_most_popular_items(self) -> list[WebElement]:
        """
        Return a sorted list of the links (WebElements) from the
        'Most Popular Items' section of the page's 'Trending' tab
        """

        MOST_POPULAR_ITEM_LINKS = (
            By.XPATH,
            "//span[@ng-repeat='popularSearch in popularSearches']/a")

        self.click_link("Trending")

        most_popular_items = self.driver.find_elements(
            *MOST_POPULAR_ITEM_LINKS)

        return sorted(most_popular_items, key=lambda item: item.text)

    def get_most_popular_items_link_text_and_href(self) -> list[list[str]]:
        """
        Return a sorted list of the links from the 'Most Popular Items' section
        of the page's 'Trending' tab

        Each element in the list is itself a list of the link text and the
        'href' attribute for a given link.
        """

        most_popular_items = self.get_most_popular_items()

        return [[item.text, item.get_attribute("href")]
                for item in most_popular_items]

    def set_entries_per_page_to(self, desired_entries_per_page: int) -> None:
        """
        Set the entries per page, using the 'Show {20/50/100} entries' dropdown
        selector
        """

        # The "Show {20/50/100} entries" dropdown selector
        NUM_ENTRIES_SELECTOR = (By.NAME, "serverSideDataTable_length")

        entriesPerPageElement = self.wait.until(
            EC.presence_of_element_located(NUM_ENTRIES_SELECTOR))

        # Change the selected number of entries to display per page
        Select(entriesPerPageElement).select_by_visible_text(
            str(desired_entries_per_page))

    def search_and_set_entries_per_page(
            self,
            searchKey: str,
            entriesPerPage: Optional[int] = None) -> None:
        """Search for the specified search key and set the entries per page"""

        self.enter_search_key(searchKey)
        self.wait_for_spinner_to_come_and_go()

        if entriesPerPage is not None:
            self.set_entries_per_page_to(entriesPerPage)
            self.wait_for_spinner_to_come_and_go()

    def get_elements_from_column(self, column_name: str) -> list[WebElement]:
        """Get all WebElements from the specified column"""

        COLUMN_XPATH_LOCATORS = {
            "make":
            "//span[@class='make-items']//a",
            "model":
            "//span[@data-uname='lotsearchLotmodel' and not(text()='[[ lm ]]')]",
            "damage":
            ("//span[@data-uname='lotsearchLotdamagedescription' and " +
             "not(text()='[[ dd ]]')]")
        }

        return self.driver.find_elements(By.XPATH,
                                         COLUMN_XPATH_LOCATORS[column_name])

    def get_web_element_value_counts(self, elements) -> dict[str, int]:
        """
        Get counts for each of the distinct text values from the specified
        WebElements
        """

        web_element_value_counts = {}

        for element in elements:

            # Specifying just element.text instead of
            #   element.get_attribute("textContent") wouldn't always work here.
            # That's because (even maximized) on a smaller (1280x1024) monitor,
            #   the DAMAGE column is scrolled out of view.
            # And there's no scrollbar to easily scroll it into view,
            #   so 'element.text' just returns blank text for that column.
            # As a result, Challenge 5, Part 2 would report 100 occurrences
            #   of category "MISC" (blank text is grouped under "MISC").
            # See https://sqa.stackexchange.com/questions/42907/ +
            #   how-to-get-text-from-an-element-when-gettext-fails
            elementKey = element.get_attribute("textContent")

            count = web_element_value_counts.get(elementKey, 0)
            web_element_value_counts[elementKey] = count + 1

        return web_element_value_counts

    def print_web_element_value_counts(self, test_title: str,
                                       web_element_value_counts) -> None:
        """
        Prints the count for each of the distinct text values from the
        specified WebElements
        """

        print(test_title)
        for key, count in web_element_value_counts.items():
            print(f"{key} - {count}")

    def search_set_entries_getcvc(self, search_key: str, entries_per_page: int,
                                  column_name: str) -> dict[str, int]:
        """
        Search for the specified search key, set the entries per page, get all
        WebElements from the specified column, and get counts for each of the
        distinct values for that column
        """

        self.search_and_set_entries_per_page(search_key, 100)
        elements = self.get_elements_from_column(column_name)
        column_value_counts = self.get_web_element_value_counts(elements)

        return column_value_counts

    def filter_button_x_path(self, panel_link_text: str):
        return f"//h4[@class='panel-title']/a[text()='{panel_link_text}']"

    def click_filter_btn(self, panel_link_text: str) -> None:
        """
        Click the specified filter button in the page's left-hand
        'Filter Options' sidebar.

        For example, click the button which expands the 'Model' filter
        """

        x_path = self.filter_button_x_path(panel_link_text)
        filter_button = self.driver.find_element(By.XPATH, x_path)
        filter_button.click()

    def set_filter_text_box(self, panel_link_text: str,
                            filter_text: str) -> None:
        """
        Enter the specified filter text (e.g., 'skyline') in the specified
        filter text box (e.g., the filter panel's 'Model' text box)
        """

        x_path = (f"{self.filter_button_x_path(panel_link_text)}" +
                  "/ancestor::li//form//input")
        filter_text_box = self.driver.find_element(By.XPATH, x_path)
        filter_text_box.send_keys(filter_text)

    def check_filter_check_box(self, panel_link_text: str,
                               filter_check_box: str) -> None:
        """
        Check the specified checkbox

        For example, check the 'Model' filter's 'Skyline' checkbox
        """

        x_path = (f"{self.filter_button_x_path(panel_link_text)}" +
                  f"/ancestor::li//ul//input[@value='{filter_check_box}']")
        check_box = self.driver.find_element(By.XPATH, x_path)
        check_box.click()

    def set_filter_text_and_check_box(self, filter_panel_link_text: str,
                                      filter_text: str,
                                      filter_check_box: str) -> bool:
        """
        In the page's page's left-hand 'Filter Options' sidebar:
            - Click the panel with the specified link text (e.g., 'Model')
            - Enter the specified text (e.g. 'skyline') in the 'Model' filter
              panel's text box
            - Check the specified checkbox (e.g. 'Skyline') in the 'Model'
              filter panel's list of checkboxes
        """

        success = True

        try:
            # Click the panel with the specified link text (e.g., 'Model')
            self.click_filter_btn(filter_panel_link_text)

            # Enter the specified text (e.g. 'Skyline') in the corresponding
            # filter text box
            self.set_filter_text_box(filter_panel_link_text, filter_text)

            # Check the corresponding filter check box
            self.check_filter_check_box(filter_panel_link_text,
                                        filter_check_box)

        except (ElementNotInteractableException, NoSuchElementException,
                TimeoutException) as error:

            # Screenshot functionality for Challenge 6
            SeleniumScreenshots(
                self.driver,
                f"{PytestServices().get_pytest_name_with_timestamp()}.png"
            ).take_screenshot()

            error_message = (
                f"\nfilter checkbox for panel: {filter_panel_link_text}, " +
                f"text: {filter_text}, checkbox: {filter_check_box} not found."
            )
            print(error_message)
            print(f"Exception {error.__class__} occurred.")

            return False

        return success
