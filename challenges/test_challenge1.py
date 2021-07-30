"""
Challenge 1 - Within test_challenge1.py, write a new test that does the
following:
1. Go to google.com
2. Search for “puppies”
3. Assert that the results page that loads has “puppies” in its title

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge1.py
"""

# Custom imports
from pages.google_search import GoogleSearchPage


def test_google_search(driver, wait):

    SEARCH_KEY = "puppies"

    # GIVEN the Google search page is displayed
    search_page = GoogleSearchPage(driver, wait)

    # WHEN the user searches for the specified search phrase
    search_page.enter_search_key(SEARCH_KEY)

    # THEN the page title of the search results contains the specified search
    # phrase
    assert SEARCH_KEY in search_page.page_title()
