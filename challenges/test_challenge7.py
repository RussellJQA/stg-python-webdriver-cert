"""
Challenge 7
Create test_challenge7.py and write a test that does the following:

Go to copart.com
Look at the Makes/Models section of the page
Create a two-dimensional list that stores the names of the Make/Model as well as their URLs
Check that each element in this list navigates to the *correct* page
"""

# pip installed

import pytest_check  # Allow multiple assert failures per test
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Custom imports

from pages.copart_home import CopartHomePage
from services.pytest_services import get_pytest_name_with_timestamp
from services.selenium_expected_conditions import any_of, none_of
from services.selenium_screenshots import SeleniumScreenshots


def test_copart_most_popular_links(driver, wait):

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    # WHEN the user clicks the "Trending" tab

    search_page.select_tab_link("Trending")

    # THEN:
    #   For each Make/Model in Trending's "Most Popular Items" section
    #       Check that the link navigates to the *correct* page

    popular_items = sorted(search_page.get_most_popular_items())

    # Get original page title
    title = driver.title

    for popular_item in popular_items:

        link_text = popular_item[0]

        # Additional variations of the link_text to check
        link_text_lower = link_text.lower()
        link_text_title = link_text.title()
        link_text_upper = link_text.upper()

        # Go to the item's URL
        href = popular_item[1]
        driver.get(href)

        # Wait for the page title to change
        wait.until(none_of(EC.title_is(title)))

        # Get new page title
        title = driver.title

        pytest_name_with_timestamp = get_pytest_name_with_timestamp()

        try:
            wait.until(
                any_of(EC.title_contains(link_text),
                       EC.title_contains(link_text_lower),
                       EC.title_contains(link_text_title),
                       EC.title_contains(link_text_upper)))

            print(f"{link_text} {href} Passed")

        except TimeoutException:

            print(f"\n*** {link_text} {href} FAILED ***\n")

            SeleniumScreenshots(
                driver, f"{pytest_name_with_timestamp}_{link_text}.png"
            ).take_screenshot()

            assert_msg = (
                f"For make/model: '{link_text}', the page title ('{driver.title}') does not contain "
                +
                f"'{link_text}', '{link_text_lower}', '{link_text_title}', or '{link_text_upper}'."
            )

            pytest_check.is_true(False, assert_msg)