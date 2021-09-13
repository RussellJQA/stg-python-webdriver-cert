"""
Challenge 4 - Fibonacci (recursion)

Create test_challenge4.py and write a test that does the following:
1. Displays the Fibonnaci sequence for N numbers
2. However, print the number(s) as English words
Example: If the sequence is 18, then print "Eighteen"
Example: If the sequence is 120, then print "One Hundred Twenty"

To run this test, specify the following in a Terminal:
    pytest challenges\test_challenge4.py -s  # Disable stdout/stderr capturing
or:
    pytest challenges\test_challenge4.py -rP  # For fuller output
"""

# pip installed
import pytest
import pytest_check  # Allow multiple assert failures per test

# Custom imports
from services.expected_fibonacci_numbers import ExpectedFibonacciNumbers
from services.expected_fibonacci_words import ExpectedFibonacciWords
from services.fibonacci import Fibonacci
from services.integer_to_words import ConvertIntegerToWords

# If you want less output, you can vary the DESIRED_SEQUENCE_LENGTH below
DESIRED_SEQUENCE_LENGTH = 301  # Generates over 100,000 characters of output


@pytest.mark.parametrize("sequence_length", [DESIRED_SEQUENCE_LENGTH])
def test_fibonacci_sequence(sequence_length: int) -> None:
    actual_fibonaccis = list(
        Fibonacci().generate_fibonacci_sequence(sequence_length))
    expected_fibonaccis = ExpectedFibonacciNumbers(
    ).get_expected_fibonacci_sequence(sequence_length)
    expected_fibonaccis_as_words = ExpectedFibonacciWords(
    ).get_expected_fibonacci_words(sequence_length)

    for num in range(sequence_length):
        fibonacci_number = actual_fibonaccis[num]
        fibonacci_number_words = ConvertIntegerToWords().number_to_words(
            fibonacci_number)
        print(f"For num={num}, the Fibonacci number is {fibonacci_number:,} " +
              f"- {fibonacci_number_words}")

        expected_fibonacci_number = expected_fibonaccis[num]
        msg_1 = (f"\n\nThe Fibonncaci number for n={num} is:" +
                 f"\n\t{fibonacci_number}\nrather than:" +
                 f"\n\t{expected_fibonacci_number}\n")
        pytest_check.equal(fibonacci_number, expected_fibonacci_number, msg_1)

        expected_fibonacci_words = expected_fibonaccis_as_words[num]
        msg_2 = (f"\n\nThe Fibonncaci number for n={num} is (in words):" +
                 f"\n\t{fibonacci_number_words}\nrather than:" +
                 f"\n\t{expected_fibonacci_words}\n")
        pytest_check.equal(fibonacci_number_words, expected_fibonacci_words,
                           msg_2)
