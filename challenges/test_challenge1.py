"""
Challenge 1 - Within test_challenge1.py, write a new test that does the following:
1. Go to google.com
2. Search for “puppies”
3. Assert that the results page that loads has “puppies” in its title

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge1.py
"""

# pip installed

from selenium.common.exceptions import (ElementNotInteractableException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC

# Custom imports

from pages.google_search import GoogleSearchPage
from services.header_search import HeaderSearch
from services.pytest_services import get_pytest_name_with_timestamp
from services.selenium_screenshots import SeleniumScreenshots


def test_google_search(driver, wait):

    # GIVEN the Google search page is displayed

    search_page = GoogleSearchPage(driver, wait)
    search_page.display()

    # WHEN the user searches for the specified search phrase

    query = "puppies"

    HeaderSearch(search_page).search(query)

    # THEN the page title of the search results contains the specified search phrase

    try:
        # Wait for the page title to change
        wait.until(EC.title_contains(query))

    except (ElementNotInteractableException, TimeoutException) as error:

        SeleniumScreenshots(
            driver,
            f"{get_pytest_name_with_timestamp()}.png").take_screenshot()

        assert False, f"{query} is not in the page title {driver.title}."
