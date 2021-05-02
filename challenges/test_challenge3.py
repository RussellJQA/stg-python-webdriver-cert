"""
Challenge 3 - Create test_challenge3.py and write a test that does the following:
1. Go to copart.com
2. On the Home Page, under Most Popular Items, there is a Makes/Models section.
For each Make or Model in this section, print the name of the Make or Model with its URL (aka href) next to it
Example Output: SILVERADO - https://www.copart.com/popular/model/silverado

To run this test, specify the following in a Terminal:
    # Show stdcalls for print statements, loggins calls, etc., by disabling stdout/stderr capturing
    pytest challenges\test_challenge3.py -s
or, for fuller output:
    pytest challenges\test_challenge3.py -rP 
"""

# Custom imports

from pages.copart_home import CopartHomePage


def test_copart_most_popular(driver, wait):

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    # WHEN the user clicks the "Trending" tab

    search_page.select_tab_link("Trending")

    # THEN for each Make or Model in this section, print the name of the Make or Model with its URL (aka href) next to it

    most_popular_items = search_page.get_most_popular_items()

    print()  # spacer so the print looks prettier
    for popular_item in sorted(most_popular_items):
        print(f"{popular_item[0]} - {popular_item[1]}")