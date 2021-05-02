"""
Challenge 4 - Fibonacci (recursion)

Create test_challenge4.py and write a test that does the following:
1. Displays the fibonnaci sequence for N numbers
2. However, print the number(s) as English words
Example: If the sequence is 18, then print "Eighteen"
Example: If the seqence is 120, then print "One Hundred Twenty"

To run this test, specify the following in a Terminal:
    # Show stdcalls for print statements, loggins calls, etc., by disabling stdout/stderr capturing
    pytest challenges\test_challenge4.py -s
or, for fuller output:
    pytest challenges\test_challenge4.py -rP 
"""

import json

# pip installed

import pytest_check  # Allow multiple assert failures per test

# Custom imports

from services.fibonacci import Fibonacci
from services.numbers_to_words import ConvertNumbertoString


def compare_vs_num2words(calculated_sequence_in_words, sequence_length):
    assert len(calculated_sequence_in_words) == sequence_length
    expected_sequence = Fibonacci().get_expected_fibonacci_sequence(
        sequence_length)
    with open("test_challenge4_expected.json") as json_file:
        expected_sequence_in_num2words = json.load(json_file)

    for count in range(sequence_length):
        expected = expected_sequence_in_num2words[count]
        calculated = calculated_sequence_in_words[count]
        assert_msg = (
            f"For the generated Fibonacci sequence of length {sequence_length}"
            +
            f"there's a miscompare for the number at position {count} in the sequence."
            + f"With the numbers as words, the expected value is:" +
            f"\t{expected}" + f"and the calculated value is:" +
            f"\t{calculated}")
        pytest_check.equal(calculated, expected, assert_msg)


# This has been tested with desired_sequence_length in {20, 50, 100, 301}.
# But since desired_sequence_length==301 generates a large amount
# (over 100,000 characters) of output, we'll just use 50 below.
DESIRED_SEQUENCE_LENGTH = 50


def test_fibonacci_sequence(desired_sequence_length=DESIRED_SEQUENCE_LENGTH):

    # Get the expected Fibonacci sequence of the specified length
    expected_sequence = Fibonacci().get_expected_fibonacci_sequence(
        desired_sequence_length)

    # Calculate the Fibonacci sequence of the specified length
    calculated_sequence = list(
        Fibonacci().generate_fibonacci_sequence(desired_sequence_length))

    calculated_sequence_in_words = list(
        map(ConvertNumbertoString().number_to_words, calculated_sequence))
    print()
    for entry in calculated_sequence_in_words:
        print(entry)
    print()

    # Compare the calculated sequence with the expected sequence
    assert calculated_sequence == expected_sequence

    # Compare the calculated sequence converted to words by
    #   ConvertNumbertoString.number_to_words()
    # with the expected sequence converted to words by
    #   num2words.num2words()
    compare_vs_num2words(calculated_sequence_in_words, desired_sequence_length)