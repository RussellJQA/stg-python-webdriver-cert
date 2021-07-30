"""
This module contains CopartHomePage, the page object for Copart's home page
"""

# pip installed

from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Custom imports

from services.pytest_services import get_pytest_name_with_timestamp
from services.selenium_screenshots import SeleniumScreenshots


class CopartHomePage:

    # URL
    URL = "https://www.copart.com"

    # Element Locators
    MAIN_SEARCH_INPUT = (By.ID, "input-search")
    TABLE = (By.XPATH, "//table[@id='serverSideDataTable']")
    SPINNER = (By.XPATH, "//div[@id='serverSideDataTable_processing']")

    # The "Show {20/50/100} entries" selector
    NUM_ENTRIES_SELECTOR = (By.NAME, "serverSideDataTable_length")

    COLUMN_XPATH_LOCATORS = {
        "make":
        "//span[@class='make-items']//a",
        "model":
        "//span[@data-uname='lotsearchLotmodel' and not(text()='[[ lm ]]')]",
        "damage": ("//span[@data-uname='lotsearchLotdamagedescription' and " +
                   "not(text()='[[ dd ]]')]")
    }

    # Initializer

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.driver.get(self.URL)

    # Page Methods

    def enter_search_key(self, searchKey):
        self.driver.find_element(*self.MAIN_SEARCH_INPUT).send_keys(
            searchKey, Keys.RETURN)

    def wait_for_spinner_to_come_and_go(self):
        spinner = self.wait.until(EC.presence_of_element_located(self.SPINNER))
        self.wait.until(EC.invisibility_of_element_located(spinner))

    def get_table_text(self):
        return self.driver.find_element(*self.TABLE).text

    def click_link(self, link_text):
        self.driver.find_element(By.LINK_TEXT, link_text).click()

    def get_most_popular_items(self):
        self.click_link("Trending")
        most_popular_items = self.driver.find_elements(
            By.XPATH,
            "//span[@ng-repeat='popularSearch in popularSearches']/a")
        return sorted(most_popular_items, key=lambda item: item.text)

    def get_most_popular_items_link_text_and_href(self):
        most_popular_items = self.get_most_popular_items()
        return [[item.text, item.get_attribute("href")]
                for item in most_popular_items]

    def set_entries_per_page_to(self, desired_entries_per_page):
        entriesPerPageElement = self.wait.until(
            EC.presence_of_element_located(self.NUM_ENTRIES_SELECTOR))
        # Change the selected number of entries to display per page
        Select(entriesPerPageElement).select_by_visible_text(
            str(desired_entries_per_page))

    def search_and_set_entries_per_page(self, searchKey, entriesPerPage):
        self.enter_search_key(searchKey)
        self.wait_for_spinner_to_come_and_go()
        if entriesPerPage > 0:
            self.set_entries_per_page_to(entriesPerPage)
            self.wait_for_spinner_to_come_and_go()

    def get_elements_from_column(self, column_name):
        return self.driver.find_elements(
            By.XPATH, self.COLUMN_XPATH_LOCATORS[column_name])

    def get_column_value_counts(self, elements):
        columnValueCounts = {}
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

            count = columnValueCounts.get(elementKey, 0)
            columnValueCounts[elementKey] = count + 1
        return columnValueCounts

    def print_column_value_counts(self, test_title, column_value_counts):
        print(test_title)
        for column_name, count in column_value_counts.items():
            print(f"{column_name} - {count}")

    def click_filter_btn(self, filter_button_x_path):
        filter_button = self.driver.find_element(By.XPATH,
                                                 filter_button_x_path)
        filter_button.click()

    def set_filter_text_box(self, filter_text_box_x_path, filter_text):
        filter_text_box = self.driver.find_element(By.XPATH,
                                                   filter_text_box_x_path)
        filter_text_box.send_keys(filter_text)

    def check_filter_check_box(self, filter_check_box_x_path):
        filter_check_box = self.driver.find_element(By.XPATH,
                                                    filter_check_box_x_path)
        filter_check_box.click()

    def set_filter_text_and_check_box(self, filter_panel_link_text,
                                      filter_text, filter_check_box) -> bool:
        success = True

        try:
            filter_button_x_path = ("//h4[@class='panel-title']" +
                                    f"/a[text()='{filter_panel_link_text}']")
            self.click_filter_btn(filter_button_x_path)

            self.set_filter_text_box(
                f"{filter_button_x_path}/ancestor::li//form//input",
                filter_text)

            self.check_filter_check_box(
                f"{filter_button_x_path}" +
                f"/ancestor::li//ul//input[@value='{filter_check_box}']")

        except (ElementNotInteractableException, NoSuchElementException,
                TimeoutException) as error:

            # Screenshot functionality required for Challenge 6
            SeleniumScreenshots(
                self.driver,
                f"{get_pytest_name_with_timestamp()}.png").take_screenshot()

            error_message = (
                f"\nfilter checkbox for panel: {filter_panel_link_text}, " +
                f"text: {filter_text}, checkbox: {filter_check_box} not found."
            )
            print(error_message)
            print(f"Exception {error.__class__} occurred.")

            return False

        return success
