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

# pip installed
import pytest_check  # Allow multiple assert failures per test

# Custom imports

# Custom imports
from services.expected_fibonacci_numbers import ExpectedFibonacciNumbers
from services.expected_fibonacci_words import ExpectedFibonacciWords
from services.fibonacci import Fibonacci
from services.numbers_to_words import ConvertNumbertoString


def compare_calculated_words_vs_expected_words(
        calculated_sequence_in_words: list[str], sequence_length: int) -> None:

    assert len(calculated_sequence_in_words) == sequence_length

    max_sequence_length = ExpectedFibonacciWords().get_max_sequence_length()
    expected_sequence_in_words = ExpectedFibonacciWords(
    ).get_expected_fibonacci_words(max_sequence_length)

    for count in range(sequence_length):
        expected = expected_sequence_in_words[count]
        calculated = calculated_sequence_in_words[count]
        assert_msg = (
            f"For the generated Fibonacci sequence of length {sequence_length}"
            +
            f" there's a miscompare for the number at position {count} in the"
            + " sequence. With the numbers as words, the expected value is:" +
            f"\t{expected} and the calculated value is:\t{calculated}")
        pytest_check.equal(calculated, expected, assert_msg)


# If you want less output, you can vary the DESIRED_SEQUENCE_LENGTH below
DESIRED_SEQUENCE_LENGTH = 301  # Generates over 100,000 characters of output


def test_fibonacci_sequence(
        desired_sequence_length: int = DESIRED_SEQUENCE_LENGTH) -> None:

    # Get the expected Fibonacci sequence of the specified length
    expected_sequence = ExpectedFibonacciNumbers(
    ).get_expected_fibonacci_sequence(desired_sequence_length)

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
    # with the expected sequence converted to words.
    compare_calculated_words_vs_expected_words(calculated_sequence_in_words,
                                               desired_sequence_length)
