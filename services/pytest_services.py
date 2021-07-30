"""
This module contains some functions for interacting with the pytest test
framework
"""

import datetime
import os


def get_current_pytest_test_name() -> str:

    # For PYTEST_CURRENT_TEST=
    #   challenges/test_challenge6.py::test_search_for_make_and_model (call)
    # the current pytest test name is "test_search_for_make_and_model"
    current_pytest_test_name = os.environ.get("PYTEST_CURRENT_TEST").split(
        ':')[-1].split(' ')[0]

    return current_pytest_test_name


def get_pytest_name_with_timestamp() -> str:
    # Append a current timestamp to the pytest Test Name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{get_current_pytest_test_name()}_{timestamp}"
