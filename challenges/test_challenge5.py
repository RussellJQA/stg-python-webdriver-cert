"""
Challenge 5

*** To run both Parts 1 and 2 of this test together, specify the following in a Terminal:
    # Show stdcalls for print statements, loggins calls, etc., by disabling stdout/stderr capturing
    pytest challenges\test_challenge5.py -s
or, for fuller output:
    pytest challenges\test_challenge5.py -rP 

*** Part 1 - Create test_challenge5.py and write a test that does the following:

1. Go to copart.com
2. Search for "porsche"
3. Change Show Entries to 100
4. Print the number of occurrences for each Model
Example: There might be x3 PANAMERA T and x11 CAYENNE

To run just Part 1 of this test, specify the following in a Terminal:
    pytest -k print_models_for_given_make -s
or, for fuller output:
    pytest -k print_models_for_given_make -rP 
The -rP reporting option gives the full output of passing tests [including print() statements]

*** Part 2 - Using the same, first three steps of Part 1, write a test that then does the following:

1. Count the number of occurrences of each Damage type
2. However, you need to map the Damage types to these:
• REAR END
• FRONT END
• MINOR DENT/SCRATCHES
• UNDERCARRIAGE
3. Any Damage type that does NOT match the above types should be grouped into a MISC Damage type
• Example: SIDE and ALL OVER would each count towards MISC
• Example Output: REAR END: 2, FRONT END: 7, MINOR DENT/SCRATCHES: 22, UNDERCARRIAGE: 0, MISC: 4

To run just Part 2 of this test, specify the following in a Terminal:
    pytest -k print_damage_for_given_make -s
or, for fuller output:
    pytest -k print_damage_for_given_make -rP
"""

from collections import Counter

# Custom imports

from pages.copart_home import CopartHomePage
from services.header_search import HeaderSearch
from services.copart_search_results_page import CopartSearchResultsPage


# Because the DAMAGE column is scrolled out of view,
# (with no scrollbar to easily scroll it back into view)
# 'span.text' just returns blank text for it.
# So, we need to use 'span.get_attribute("textContent")' instead.
# See https://sqa.stackexchange.com/questions/42907/ +
#   how-to-get-text-from-an-element-when-gettext-fails
def get_counts(spans) -> Counter:
    counts = Counter()
    for span in spans:
        key = span.get_attribute("textContent")
        counts.update({key: 1})
    return counts


# Challenge 5, Part 1
def test_print_models_for_given_make(driver, wait):

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    # WHEN the user searches the Copart home page for "porsche"
    #   AND then changes Show Entries to 100

    query = "porsche"

    HeaderSearch(search_page).search(query)

    results_per_page = CopartSearchResultsPage(search_page)
    results_per_page.set_results_per_page(100)

    # THEN Print the number of occurrences for each Model
    #   Example: ... CAYENNE: 16, ... PANAMERA T: 2, ...

    # Get the span elements for the "Model" column of the search results table
    spans = search_page.driver.find_elements(
        *CopartHomePage.td_span_locator("model"))

    # Count the number of entries of each model in the table rows
    models = get_counts(spans)

    # Print models Counter, but ordered alphabetically (except with "ALL OTHER" at the end)
    models_list = sorted(list(set(models) - {"ALL OTHER"})) + ["ALL OTHER"]
    print()
    print(", ".join('{}: {}'.format(model, models[model])
                    for model in models_list))
    print()


# Challenge 5, Part 2
def test_print_damage_for_given_make(driver, wait):
    """ Summarize damage information for all vehicles of the specified make """

    # GIVEN the Copart home page is displayed

    search_page = CopartHomePage(driver, wait)
    search_page.display()

    # WHEN the user searches the Copart home page for "porsche"
    #   AND then changes Show Entries to 100

    query = "porsche"

    HeaderSearch(search_page).search(query)

    results_per_page = CopartSearchResultsPage(search_page)
    results_per_page.set_results_per_page(100)

    # THEN Print the number of occurrences of each Damage type
    #   Example: FRONT END: 49, REAR END: 12, MINOR DENT/SCRATCHES: 5, UNDERCARRIAGE: 2, MISC: 32

    # Get the span elements for the "Damage" column of the search results table
    spans = driver.find_elements(
        *CopartHomePage.td_span_locator("damagedescription"))

    MAIN_DAMAGE_TYPES = [
        "FRONT END", "REAR END", "MINOR DENT/SCRATCHES", "UNDERCARRIAGE"
    ]

    damages = get_counts(spans)

    # Group all damages not contained in MAIN_DAMAGE_TYPES as "MISC"
    damages_grouped = Counter()
    for damage in damages:
        damages_grouped.update({
            (damage if damage in MAIN_DAMAGE_TYPES else "MISC"):
            damages[damage]
        })

    # Print damages Counter (but in the order of MAIN_DAMAGE_TYPES) + f", MISC: {misc_count}"
    print()
    print(", ".join('{}: {}'.format(damage_type, damages_grouped[damage_type])
                    for damage_type in (MAIN_DAMAGE_TYPES + ["MISC"])))
    print()
