"""
Challenge 7
Create test_challenge7.py and write a test that does the following:

Go to copart.com
Look at the Makes/Models section of the page
Create a two-dimensional list that stores the names of the Make/Model as well
as their URLs
Check that each element in this list navigates to the *correct* page

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge7.py -s  # Disable stdout/stderr capturing
or:
    pytest challenges\test_challenge7.py -rP  # For fuller output
"""

# pip installed
import pytest_check  # Allow multiple assert failures per test
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Custom imports
from pages.copart_home import CopartHomePage


def test_navigate_through_most_popular_items(driver: WebDriver,
                                             wait: WebDriverWait):
    # GIVEN the Copart homepage is displayed
    copart_page = CopartHomePage(driver, wait)

    # WHEN you get a list of the link text and the hrefs for the page's
    # "Most Popular Items", and navigate to each href in the list
    most_popular_items_link_info = (
        copart_page.get_most_popular_items_link_info())

    for link_info in most_popular_items_link_info:
        link_text = link_info.link_text
        href = link_info.href
        print(f"Make or model: {link_text}, href: {href}")
        driver.get(href)

        # THEN For each element in the list, the current URL of the navigated-to page contains the element's link text

        make1 = link_text.lower()
        make2 = make1.replace(" ", "-")  # Handle US's "3 SERIES"
        make3 = make1.replace(" ", "")  # Handle UK's "LAND ROVER" and "MERCEDES BENZ"
        make4 = make1.replace("-", "")  # Handle Canada's "MERCEDES-BENZ"

        pytest_check.is_true(
            (make1 in driver.current_url or make2 in driver.current_url or
             make3 in driver.current_url or make4 in driver.current_url),
            f"\n\nThe link text (lower-cased) '{link_text.lower()}' is not in "
            + f"the current URL '{driver.current_url}'\n")
