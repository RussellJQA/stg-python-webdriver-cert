"""
Challenge 5

*** To run both Parts 1 and 2 of this test together, specify the following in
        a Terminal:
   pytest challenges\test_challenge5.py -s
or, for fuller output:
    pytest challenges\test_challenge5.py -rP

*** Part 1 - Create test_challenge5.py and write a test that does the
following:

1. Go to copart.com
2. Search for "porsche"
3. Change Show Entries to 100
4. Print the number of occurrences for each Model
Example: There might be x3 PANAMERA T and x11 CAYENNE

To run just Part 1 of this test, specify the following in a Terminal:
    pytest -k print_models_for_given_make -s
or, for fuller output:
    pytest -k print_models_for_given_make -rP
The -rP reporting option gives the full output of passing tests
[including print() statements]

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

To run just Part 2 of this test, specify the following in a Terminal:
    pytest -k print_damage_for_given_make -s
or, for fuller output:
    pytest -k print_damage_for_given_make -rP
"""

from collections import Counter

# pip installed

import pytest

# Custom imports

from pages.copart_home import CopartHomePage

# Challenge 5, Part 1


@pytest.mark.parametrize("search_key", ["porsche"])
def test_print_porsche_models(driver, wait, search_key):

    # GIVEN the Copart homepage is displayed
    copart_homepage = CopartHomePage(driver, wait)

    # WHEN the user searches for the specified search phrase,
    # and sets the entries per page to 100
    copart_homepage.search_and_set_entries_per_page(search_key, 100)

    # THEN Print PORSCHE models

    elements = copart_homepage.get_elements_from_column("model")
    column_value_counts = copart_homepage.get_column_value_counts(elements)

    # Sort dict into a list, alphabetically except with "MISC" last
    sorted_column_value_counts_items = sorted(
        column_value_counts.items(), key=lambda key_value: key_value[0])

    test_title = (
        f"\nPART 1: {len(column_value_counts)} distinct " +
        f"{search_key.upper()} MODELS (with counts of their occurrences)")

    # dict() used to convert the list back into a dict
    copart_homepage.print_column_value_counts(
        test_title, dict(sorted_column_value_counts_items))


# Challenge 5, Part 2


@pytest.mark.parametrize("search_key", ["porsche"])
def test_print_porsche_damages(driver, wait, search_key):

    # GIVEN the Copart homepage is displayed
    copart_homepage = CopartHomePage(driver, wait)

    # WHEN the user searches for the specified search phrase,
    # and sets the entries per page to 100
    copart_homepage.search_and_set_entries_per_page(search_key, 100)

    # THEN Print PORSCHE damages

    elements = copart_homepage.get_elements_from_column("damage")
    column_value_counts = copart_homepage.get_column_value_counts(elements)

    # Group all damages not contained in MAIN_DAMAGE_TYPES as "MISC"
    MAIN_DAMAGE_TYPES = [
        "FRONT END", "REAR END", "MINOR DENT/SCRATCHES", "UNDERCARRIAGE"
    ]
    damages_grouped = Counter()
    for damage in dict(column_value_counts):
        damages_grouped.update({
            (damage if damage in MAIN_DAMAGE_TYPES else "MISC"):
            dict(column_value_counts)[damage]
        })

    # Sort dict into a list, alphabetically except with "MISC" last
    sorted_column_value_counts_items = sorted(
        damages_grouped.items(),
        key=lambda key_value: ("ZZZZZ"
                               if (key_value[0] == "MISC") else key_value[0]))

    test_title = (
        f"\nPART 2: {len(sorted_column_value_counts_items)} " +
        f"{search_key.upper()} Damage Types (with counts of their occurrences)"
    )

    # dict() used to convert the list back into a dict
    copart_homepage.print_column_value_counts(
        test_title, dict(sorted_column_value_counts_items))
