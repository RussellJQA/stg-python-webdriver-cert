"""
This module creates a .json file containing the Fibonacci sequence of the
maximum length supported by the Fibonacci class, with the numbers of the
sequence (0, 1, 1, 2, 3, ...)
converted to words  ("zero", "one", "one", "two", "three", ...)
"""

import json

# pip installed

# Used only to generate expected results for challenge 4
from num2words import num2words

# Custom imports

from services.fibonacci import Fibonacci

fibonacci = Fibonacci()
sequence_length = fibonacci.max_sequence_length
expected_sequence = Fibonacci().get_expected_fibonacci_sequence(
    sequence_length)

# Generate the expected sequence, in words, using a slight different format
#   then num2words.
# For example, where num2words has:
#   twelve billion, five hundred and eighty-six million,
#       two hundred and sixty-nine thousand and twenty-five
# this will instead have:
#   twelve billion, five hundred eighty six million,
#       two hundred sixty nine thousand and twenty five
expected_sequence_as_words = [
    num2words(num).replace(" and ", " ").replace("-", " ")
    for num in expected_sequence
]

with open("test_challenge4_expected.json", "w") as write_file:
    json.dump(expected_sequence_as_words, write_file, indent=4)
