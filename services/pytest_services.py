"""
The PytestServices class contains some functions for interacting with the
pytest test framework.
"""

import datetime
import os


class PytestServices:
    @staticmethod
    def get_current_pytest_test_name() -> str:
        # For PYTEST_CURRENT_TEST=
        #  challenges/test_challenge6.py::test_search_for_make_and_model (call)
        # the current pytest test name is "test_search_for_make_and_model"
        pytest_current_test = str(os.environ.get("PYTEST_CURRENT_TEST"))
        current_pytest_test_name = pytest_current_test.split(':')[-1].split(' ')[0]

        return current_pytest_test_name

    def get_pytest_name_with_timestamp(self) -> str:
        # Append a current timestamp to the pytest Test Name
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{self.get_current_pytest_test_name()}_{timestamp}"
