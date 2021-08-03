"""
Challenge 4 - Fibonacci (recursion)

Create test_challenge4.py and write a test that does the following:
1. Displays the fibonnaci sequence for N numbers
2. However, print the number(s) as English words
Example: If the sequence is 18, then print "Eighteen"
Example: If the seqence is 120, then print "One Hundred Twenty"

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge4.py -s
or, for fuller output:
    pytest challenges\test_challenge4.py -rP
"""

# Import Python 3.9+'s ability to type hint lists and dictionaries directly
# into 3.7 <= Python < 3.9. Without this, you need to use
# "from typing import List" along with "List[int]", "List[str]",
# "from typing import Dict" along with "dict[str, int]", etc.
from __future__ import annotations

# pip installed
import pytest_check  # Allow multiple assert failures per test

# Custom imports

# Custom imports
from services.expected_fibonacci_numbers import ExpectedFibonacciNumbers
from services.expected_fibonacci_words import ExpectedFibonacciWords
from services.fibonacci import Fibonacci
from services.numbers_to_words import ConvertNumbertoString


def compare_actual_vs_expected(
        sequence_length: int, calculated_sequence_in_numbers: list[int],
        calculated_sequence_in_words: list[str]) -> None:

    expected_sequence_in_numbers = ExpectedFibonacciNumbers(
    ).get_expected_fibonacci_sequence(sequence_length)

    expected_sequence_in_words = ExpectedFibonacciWords(
    ).get_expected_fibonacci_words(sequence_length)

    for count in range(sequence_length):

        actual_number = calculated_sequence_in_numbers[count]
        expected_number = expected_sequence_in_numbers[count]
        assert_msg1 = (f"\n\nThe Fibonncaci number for n={count} is:" +
                       f"\n\t{actual_number}\nrather than " +
                       f"\n\t{expected_number}\n")
        pytest_check.equal(actual_number, expected_number, assert_msg1)

        actual_words = calculated_sequence_in_words[count]
        expected_words = expected_sequence_in_words[count]
        assert_msg2 = (
            f"\n\nThe Fibonncaci number for n={count} is (in words):" +
            f"\n\t{actual_words}\nrather than " + f"\n\t{expected_words}\n")
        pytest_check.equal(actual_words, expected_words, assert_msg2)


# If you want less output, you can vary the DESIRED_SEQUENCE_LENGTH below
DESIRED_SEQUENCE_LENGTH = 301  # Generates over 100,000 characters of output


def test_fibonacci_sequence(
        desired_sequence_length: int = DESIRED_SEQUENCE_LENGTH) -> None:

    # Calculate the Fibonacci sequence of the specified length
    calculated_sequence_in_numbers = list(
        Fibonacci().generate_fibonacci_sequence(desired_sequence_length))

    calculated_sequence_in_words = list(
        map(ConvertNumbertoString().number_to_words,
            calculated_sequence_in_numbers))
    print()
    for entry in calculated_sequence_in_words:
        print(entry)
    print()

    compare_actual_vs_expected(desired_sequence_length,
                               calculated_sequence_in_numbers,
                               calculated_sequence_in_words)
