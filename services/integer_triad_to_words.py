"""
The ConvertIntegerTriadToWords utility class is used to convert an integer triad
[1-to-3-digit integer,
 or 1-to-3-digit portion of a larger integer (representing either the thousands, millions, billions, or ... place)]
(e.g., 629) to its corresponding strings of words (e.g., "six hundred twenty nine").
"""

NUM_LT_TWENTY = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen"
}


class ConvertIntegerTriadToWords:

    @staticmethod
    def get_words_for_tens_and_ones_digits(one_to_three_digit_int: int,
                                           hundreds_digit: int) -> str:

        TENS_PLACE = {
            10: "ten",
            20: "twenty",
            30: "thirty",
            40: "forty",
            50: "fifty",
            60: "sixty",
            70: "seventy",
            80: "eighty",
            90: "ninety"
        }

        tens_and_ones = int(one_to_three_digit_int - (100 * hundreds_digit))

        if tens_and_ones > 19:
            tens_digit = int(tens_and_ones // 10)
            ones_digit = int(tens_and_ones - 10 * tens_digit)
            return ((" " if hundreds_digit else "") +
                    f"{TENS_PLACE[10 * tens_digit]}" +
                    (f" {NUM_LT_TWENTY[ones_digit]}" if ones_digit else ""))
        else:
            return "" if (tens_and_ones == 0) else f" {NUM_LT_TWENTY[tens_and_ones]}"

    @staticmethod
    def triad_to_string(one_to_three_digit_int: int) -> str:

        if one_to_three_digit_int < 0 or one_to_three_digit_int > 999:
            raise ValueError(f"The input {str(one_to_three_digit_int)} should be a 1-to-3 digit integer.")

        HUNDREDS_PLACE = {
            100: "one hundred",
            200: "two hundred",
            300: "three hundred",
            400: "four hundred",
            500: "five hundred",
            600: "six hundred",
            700: "seven hundred",
            800: "eight hundred",
            900: "nine hundred"
        }

        if one_to_three_digit_int <= 19:
            return "" if one_to_three_digit_int == 0 else NUM_LT_TWENTY[one_to_three_digit_int]

        if one_to_three_digit_int >= 100:
            hundreds_digit = (one_to_three_digit_int // 100)
            result = HUNDREDS_PLACE[100 * hundreds_digit]
        else:
            hundreds_digit = 0
            result = ""

        result += ConvertIntegerTriadToWords().get_words_for_tens_and_ones_digits(
            one_to_three_digit_int, hundreds_digit)

        return result
