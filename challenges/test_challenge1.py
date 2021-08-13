"""
Challenge 1 - Within test_challenge1.py, write a new test that does the
following:
1. Go to google.com
2. Search for “puppies”
3. Assert that the results page that loads has “puppies” in its title

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge1.py
"""

# pip installed
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Custom imports
from pages.google_search import GoogleSearchPage


# Search for "“puppies”"
@pytest.mark.parametrize("search_key", ["puppies"])
def test_google_search(driver: WebDriver, wait: WebDriverWait,
                       search_key: str) -> None:
    # GIVEN the Google search page is displayed
    search_page = GoogleSearchPage(driver, wait)

    # WHEN the user searches for the specified search phrase
    search_page.enter_search_key(search_key)

    # THEN the page title of the search results contains the specified search
    # phrase
    assert search_key in search_page.page_title()
