"""
The Fibonacci class has functions for dealing with Fibonacci numbers, and
Fibonacci sequences. For an explanation of Fibonacci numbers and Fibonacci
sequences, see https://en.wikipedia.org/wiki/Fibonacci_number.
"""

from typing import Generator

# Custom imports
from services.expected_fibonacci_numbers import ExpectedFibonacciNumbers


class Fibonacci:
    expected_fibonacci_sequence = ExpectedFibonacciNumbers(
    ).get_expected_fibonacci_sequence(301)

    # Cache of known Fibonacci numbers
    known_cache = {
        0: expected_fibonacci_sequence[0],
        1: expected_fibonacci_sequence[1]
    }

    def get_fibonacci_number(self, n: int) -> int:
        """Recursively generate the nth Fibonacci number"""

        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")

        if n in self.known_cache:
            return self.known_cache[n]

        # Without caching known Fibonacci numbers like this, this function
        # will generate a "maximum recursion depth exceeded" error
        # (when for sufficiently large Fibonacci numbers).
        # That's because Python doesn't do tail recursion elimination.
        self.known_cache[n] = self.get_fibonacci_number(
            n - 1) + self.get_fibonacci_number(n - 2)

        return self.known_cache[n]

    def generate_fibonacci_sequence(
            self, sequence_length: int) -> Generator[int, None, None]:

        if not isinstance(sequence_length, int) or sequence_length < 1:
            raise ValueError("sequence_length must be a positive integer")

        return (self.get_fibonacci_number(n) for n in range(sequence_length))
