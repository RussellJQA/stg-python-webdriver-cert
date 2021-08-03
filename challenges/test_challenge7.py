"""
Challenge 7
Create test_challenge7.py and write a test that does the following:

Go to copart.com
Look at the Makes/Models section of the page
Create a two-dimensional list that stores the names of the Make/Model as well
as their URLs
Check that each element in this list navigates to the *correct* page

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge7.py -s
or, for fuller output:
    pytest challenges\test_challenge7.py -rP
"""

# pip installed

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
    most_popular_items_link_text_and_href = (
        copart_page.get_most_popular_items_link_text_and_href())

    for item in most_popular_items_link_text_and_href:
        link_text = item[0]
        href = item[1]
        print(f"Make or model: {item[0]}, href: {href}")
        driver.get(href)

        # THEN for each element in the list, the current URL of the
        # navigated-to page contains the element's link text (lower-cased)
        assert (link_text.lower() in driver.current_url)
