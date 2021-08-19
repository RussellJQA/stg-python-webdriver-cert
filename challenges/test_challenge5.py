"""
Challenge 5

*** To run both Parts 1 and 2 of this test together, specify the following in
        a Terminal:
    pytest challenges\test_challenge5.py -s  # Disable stdout/stderr capturing
or:
    pytest challenges\test_challenge5.py -rP  # For fuller output

*** Part 1 - Create test_challenge5.py and write a test that does the
following:

1. Go to copart.com
2. Search for "porsche"
3. Change Show Entries to 100
4. Print the number of occurrences for each Model
Example: There might be x3 PANAMERA T and x11 CAYENNE

*** Part 2 - Using the same, first three steps of Part 1, write a test that
then does the following:

1. Count the number of occurrences of each Damage type
2. However, you need to map the Damage types to these:
• REAR END
• FRONT END
• MINOR DENT/SCRATCHES
• UNDERCARRIAGE
3. Any Damage type that does NOT match the above types should be grouped into
a MISC Damage type
• Example: SIDE and ALL OVER would each count towards MISC
• Example Output: REAR END: 2, FRONT END: 7, MINOR DENT/SCRATCHES: 22,
    UNDERCARRIAGE: 0, MISC: 4
"""

# Import Python 3.9+'s ability to type hint lists and dictionaries directly
# into 3.7 <= Python < 3.9. Without this, you need to use
# "from typing import List" along with "List[int]", "List[str]",
# "from typing import Dict" along with "dict[str, int]", etc.

from __future__ import annotations

# pip installed
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Custom imports
from pages.copart_home import CopartHomePage

testdata = [
    ("porsche", "model", []),  # Challenge 5, Part 1
    ("porsche", "damage", [
        "MISC", "FRONT END", "REAR END", "MINOR DENT/SCRATCHES",
        "UNDERCARRIAGE"
    ])  # Challenge 5, Part 2
]


@pytest.mark.parametrize("search_key, column_name, column_lumping", testdata)
def test_search_then_print_column_data(driver: WebDriver, wait: WebDriverWait,
                                       search_key: str, column_name: str,
                                       column_lumping: list[str]) -> None:
    """Search copart.com for specified search key, then print distinct values of specified search results column

    Args:
        driver: Selenium WebDriver instance to use in this test [set by pytest driver() fixture]
        wait: Selenium WebDriverWait instance to use in this test [set by pytest driver() fixture]
        search_key: search phrase (e.g., "porsche") to enter into Copart.com's main search box
        column_name: lowercase name of the column (in Copart.com's search results table)
            whose distinct values this test should print out (with counts of their occurrences)
            (e.g., "model" or "damage")
        column_lumping: Information on how to "lump" "miscellaneous" values for that column:
            column_lumping[0]: A named category (such as "MISC") to lump "miscellaneous" values into
            column_lumping[1:] Those distinct values which won't be lumped into "MISC"

            For example, column_lumping=["MISC", "FRONT END", "REAR END", "MINOR DENT/SCRATCHES", "UNDERCARRIAGE"]
                will lump all values other than "FRONT END", "REAR END", "MINOR DENT/SCRATCHES", and "UNDERCARRIAGE"
                together as "MISC"

            If len(column_lumping) == 0, then no lumping will occur. Instead, all distinct values will be reported.
    """

    # See https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html re: docstring format

    # GIVEN the Copart homepage is displayed
    copart_homepage = CopartHomePage(driver, wait)

    # WHEN the user:
    # • Searches for the specified search phrase (e.g., "porsche"),
    # • Sets the entries per page (e.g., to 100), and get counts for each of the distinct values for a specified column
    #     (e.g., "damage")
    column_value_counts = copart_homepage.search_set_entries_getcvc(
        search_key, 100, column_name.lower())

    # THEN Get and print a sorted list of those values, with their corresponding counts

    test_title = (
        f"\n{search_key.upper()} " +
        f"{column_name.lower()} values (with counts of their occurrences)")

    if len(column_lumping) < 2:
        sorted_column_value_counts_items = sorted(
            column_value_counts.items(),
            key=lambda key_value: key_value[0])  # Sort dict into a list
    else:
        sorted_column_value_counts_items = copart_homepage.get_lumped_and_sorted_column_value_counts_items(
            column_value_counts, column_lumping)

    # dict() used to convert the list back into a dict
    copart_homepage.print_web_element_value_counts(
        test_title, dict(sorted_column_value_counts_items))
