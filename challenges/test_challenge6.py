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


def test_search_for_make_and_model(driver, wait):

    SEARCH_KEY = "nissan"
    FILTER_PANEL_LINK_TEXT = "Model"
    FILTER_TEXT = "skyline"
    FILTER_CHECK_BOX = "Skyline"

    # GIVEN the Copart homepage is displayed
    copart_page = CopartHomePage(driver, wait)

    # WHEN the user searches for the specified search phrase
    copart_page.enter_search_key(SEARCH_KEY)
    copart_page.wait_for_spinner_to_come_and_go()

    assert copart_page.set_filter_text_and_check_box(FILTER_PANEL_LINK_TEXT,
                                                     FILTER_TEXT,
                                                     FILTER_CHECK_BOX)
