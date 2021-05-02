"""
Challenge 2 - Create test_challenge2.py and write a test that does the following:
1. Go to copart.com
2. Search for "exotics"
3. Assert "PORSCHE" is in the list of cars on the Results Page

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge2.py
"""

# pip installed

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Custom imports

from pages.copart_home import CopartHomePage
from services.copart_search_results_page import CopartSearchResultsPage
from services.header_search import HeaderSearch
from services.pytest_services import get_pytest_name_with_timestamp
from services.selenium_screenshots import SeleniumScreenshots


def test_copart_search(driver, wait):

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    # WHEN the user searches the Copart home page for "exotics"

    query = "exotics"

    HeaderSearch(search_page).search(query)

    # THEN "PORSCHE" is in the list of vehicles on the Results Page

    # Wait for search results to be loaded
    CopartSearchResultsPage(search_page).wait_for_search_results_to_be_loaded()

    MAKE_TO_LOCATE = "PORSCHE"

    try:
        matching_span = wait.until(
            EC.presence_of_element_located(
                CopartHomePage.td_span_locator(
                    "make", f"contains(text(), '{MAKE_TO_LOCATE}')")))

    except TimeoutException:

        SeleniumScreenshots(
            driver,
            f"{get_pytest_name_with_timestamp()}.png").take_screenshot()

        assert False, (MAKE_TO_LOCATE +
                       " is not in the list of vehicles on the results page")
