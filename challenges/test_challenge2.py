"""
Challenge 2 - Create test_challenge2.py and write a test that does the
following:
1. Go to copart.com
2. Search for "exotics"
3. Assert "PORSCHE" is in the list of cars on the Results Page

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge2.py
"""

# Custom imports
from pages.copart_home import CopartHomePage


def test_copart_search(driver, wait):

    SEARCH_KEY = "exotics"
    EXPECTED_SEARCH_RESULT = "PORSCHE"

    # GIVEN the Copart homepage is displayed
    search_page = CopartHomePage(driver, wait)

    # WHEN the user searches for the specified search phrase
    search_page.enter_search_key(SEARCH_KEY)
    search_page.wait_for_spinner_to_come_and_go()

    # THEN the text of the resulting table (of search results) contains the
    # specified search result
    assert EXPECTED_SEARCH_RESULT in search_page.get_table_text()
