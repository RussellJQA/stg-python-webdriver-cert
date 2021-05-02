"""
Challenge 6
Create test_challenge6.py and write a test that does the following:

Go to copart.com
Search for 'nissan'
Then for the Model, search 'skyline'. This is a rare car that might not exist
If it doesn't exist, catch the exception and take a screenshot

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge6.py
"""

# Custom imports

from pages.copart_home import CopartHomePage
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        TimeoutException)
from services.copart_filters import CopartFilters

from services.pytest_services import get_pytest_name_with_timestamp
from services.selenium_screenshots import SeleniumScreenshots


def handle_exceptions(driver, query, filter_name, filter_value,
                      results_table_search, error):
    """If there are no matches, then take a screenshot."""

    SeleniumScreenshots(
        driver, f"{get_pytest_name_with_timestamp()}.png").take_screenshot()

    assert_msg = (
        f"Unable to find any search results matching '{results_table_search}' "
        +
        f"for query='{query}', filtered by '{filter_name}'='{filter_value}'" +
        f"\nException {error.__class__} occurred.")
    assert False, assert_msg


# Challenge 6
def test_search_for_given_make_and_model(driver, wait):
    """Search for any occurrences of the specified make/model."""

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    try:

        # WHEN the user:
        #   Searches the Copart home page for "nissan"
        query = "nissan"

        # and:
        #   Filters the results for "Model"="skyline"
        filter_name = "Model"
        filter_value = "skyline"

        results_table_search = filter_value.upper()

        filters = CopartFilters(driver, wait)
        filters.do_filtered_search(driver, wait, search_page, query,
                                   filter_name, filter_value)

        # THEN the search results contain "skyline" models

        # To temporarily force a TimeOutException, change upper() to title() below
        search_page.search_results_contain(
            span_type=filter_name,
            span_match_criteria=f"contains(text(), '{results_table_search}')")

    except (ElementNotInteractableException, NoSuchElementException,
            TimeoutException) as error:
        handle_exceptions(driver, query, filter_name, filter_value,
                          results_table_search, error)


# Test that CopartFilters functions as a generic filter class,
# exercising the filters on the left hand side of the search results page.
# Filter for a filter_name other than "Model" (such as "Year").
def test_generic_copart_filters(driver, wait):
    """Search for any occurrences of the specified make/year."""

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    try:

        # WHEN the user:
        #   Searches the Copart home page for "toyota"
        query = "toyota"

        # and:
        #   Filters the results for "Year"="2020"
        filter_name = "Year"
        filter_value = "2020"

        results_table_search = filter_value

        filters = CopartFilters(driver, wait)
        filters.do_filtered_search(driver, wait, search_page, query,
                                   filter_name, filter_value)

        # THEN the search results contain "2020" vehicles

        search_page.search_results_contain(
            span_type="centuryyear",
            span_match_criteria=f"contains(text(), '{results_table_search}')")

    except (ElementNotInteractableException, NoSuchElementException,
            TimeoutException) as error:
        handle_exceptions(driver, query, filter_name, filter_value,
                          results_table_search, error)