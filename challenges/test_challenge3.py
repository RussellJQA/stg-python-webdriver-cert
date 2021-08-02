"""
Challenge 3 - Create test_challenge3.py and write a test that does the
following:
1. Go to copart.com
2. On the Home Page, under Most Popular Items, there is a Makes/Models section.
For each Make or Model in this section, print the name of the Make or Model
with its URL (aka href) next to it.
Example Output: SILVERADO - https://www.copart.com/popular/model/silverado

To run this test, specify the following in a Terminal:

    # Show stdcalls for print statements, loggins calls, etc.,
    # by disabling stdout/stderr capturing
    pytest challenges\test_challenge3.py -s

or, for fuller output:

    pytest challenges\test_challenge3.py -rP
"""

# pip installed

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Custom imports
from pages.copart_home import CopartHomePage


def test_get_list_of_most_popular_items(driver: WebDriver,
                                        wait: WebDriverWait) -> None:

    # GIVEN the Copart homepage is displayed
    copart_page = CopartHomePage(driver, wait)

    # WHEN you get a list of the Web elements for the page's
    # "Most Popular Items"
    most_popular_items = copart_page.get_most_popular_items()

    # THEN you can print the link text and href for each of the Web elements
    print()
    for item in most_popular_items:
        print(item.text + " - ", item.get_attribute("href"))
