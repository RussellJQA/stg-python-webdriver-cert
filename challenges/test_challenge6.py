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

# pip installed

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Custom imports
from pages.copart_home import CopartHomePage


@pytest.mark.parametrize(
    "search_key,filter_panel_link_text,filter_text,filter_check_box",
    [("nissan", "Model", "skyline", "Skyline")])
def test_search_for_make_and_model(driver: WebDriver, wait: WebDriverWait,
                                   search_key: str,
                                   filter_panel_link_text: str,
                                   filter_text: str, filter_check_box: str):

    # GIVEN the Copart homepage is displayed
    copart_page = CopartHomePage(driver, wait)

    # WHEN the user searches for the specified search phrase
    copart_page.enter_search_key(search_key)
    copart_page.wait_for_spinner_to_come_and_go()

    # THEN the user is able to successfully do the following
    # in the page's page's left-hand 'Filter Options' sidebar:
    #   - Click the panel with the specified link text (e.g., 'Model')
    #   - Enter the specified text (e.g. 'skyline') in the 'Model' filter
    #       panel's text box
    #   - Check the specified checkbox (e.g. 'Skyline') in the 'Model' filter
    #       panel's list of checkboxes
    assert_msg = (f"Error searching for '{search_key}', filtered by " +
                  f"'{filter_panel_link_text}'='{filter_text}' " +
                  f"with {filter_check_box} checkbox")
    assert copart_page.set_filter_text_and_check_box(
        filter_panel_link_text, filter_text, filter_check_box), assert_msg
