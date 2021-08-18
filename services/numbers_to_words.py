"""
The ConvertNumbertoString class is used to convert numbers (e.g., 21) to their
corresponding strings (e.g., "twenty one").
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


class ConvertNumbertoString:

    @staticmethod
    def get_hundreds_digit(one_to_three_digit_int: int) -> int:
        return 0 if one_to_three_digit_int < 100 else int(one_to_three_digit_int // 100)

    @staticmethod
    def get_words_for_tens_and_ones_digits(one_to_three_digit_int: int, hundreds_digit: int) -> str:

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

        tens_digit = 0 if tens_and_ones < 10 else int(tens_and_ones // 10)

        if tens_and_ones <= 19:
            if tens_and_ones:
                return f" {NUM_LT_TWENTY[tens_and_ones]}"
        else:
            ones_digit = int(tens_and_ones - 10 * tens_digit)
            if tens_digit > 0:
                return ((" " if hundreds_digit else "") +
                        f"{TENS_PLACE[10 * tens_digit]}" +
                        (f" {NUM_LT_TWENTY[ones_digit]}"
                         if ones_digit else ""))
            elif tens_digit == 0 and ones_digit != 0:
                return f" {NUM_LT_TWENTY[ones_digit]}"

        return ""

    @staticmethod
    def get_grouping_separator(triad: str, triad_group_number: int, triad_count: int) -> str:

        if triad_group_number:
            if int(triad) >= 100 or triad_group_number < triad_count - 1:
                return ", "
            else:
                return " "
        else:
            return ""

    @staticmethod
    def triad_to_string(one_to_three_digit_int: int) -> str:

        assert_msg = (f"The input {str(one_to_three_digit_int)} " +
                      "should be a 1-to-3 digit integer.")
        assert 0 <= one_to_three_digit_int <= 999, assert_msg

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

        hundreds_digit = ConvertNumbertoString().get_hundreds_digit(one_to_three_digit_int)

        result = "" if one_to_three_digit_int < 100 else HUNDREDS_PLACE[100 * hundreds_digit]

        result += ConvertNumbertoString().get_words_for_tens_and_ones_digits(one_to_three_digit_int, hundreds_digit)

        return result

    @staticmethod
    def number_to_words(number: int) -> str:
        """
        Returns the input integer number represented as a string of words.
        For example, for the integer 12586269025, it will return:
            twelve billion, five hundred eighty six million,
                two hundred sixty nine thousand twenty five
        """

        if number == 0:
            number_as_words = "zero"
        else:
            # Groupings were taken from "Names for Powers of Ten" at
            # https://amazingmathclub.wordpress.com/names-for-power-of-ten/.
            #
            # For ease of comparison with output from the
            # https://pypi.org/project/num2words/ project, where there was more
            # than 1 name to choose from, the name used by num2words was chosen

            TRIAD_GROUPINGS = {
                0: "",
                1: "thousand",
                2: "million",
                3: "billion",
                4: "trillion",
                5: "quadrillion",
                6: "quintillion",
                7: "sextillion",
                8: "septillion",
                9: "octillion",
                10: "nonillion",
                11: "decillion",
                12: "undecillion",
                13: "duodecillion",
                14: "tredecillion",
                15: "quattuordecillion",
                16: "quindecillion",
                17: "sexdecillion",
                18: "septdecillion",
                19: "octodecillion",
                20: "novemdecillion",
                21: "vigintillion"
            }

            number_as_string = str(number)
            string_length = len(number_as_string)

            # Zero-pad the string until its length is evenly divisible by 3
            padded_length = string_length + ((3 - (string_length % 3)) % 3)
            triad_count = padded_length // 3
            number_as_string_padded = number_as_string.zfill(padded_length)

            number_as_words = ""
            for triad_group_number in range(triad_count):
                triad = number_as_string_padded[3 * triad_group_number:3 * triad_group_number + 3]

                # If the current triad is not empty, then ...
                if triad != "000":
                    triad_as_string = ConvertNumbertoString().triad_to_string(int(triad))
                    triad_grouping = TRIAD_GROUPINGS[triad_count -
                                                     triad_group_number -
                                                     1]  # 6: "quintillion",

                    grouping_separator = ConvertNumbertoString().get_grouping_separator(triad, triad_group_number,
                                                                                        triad_count)
                    number_as_words += (
                            f"{grouping_separator}{triad_as_string}" +
                            (f" {triad_grouping}" if triad_grouping else ""))

        return number_as_words


if __name__ == '__main__':
    # The Fibonacci number for n=300
    num = 222232244629420445529739893461909967206666939096499764990979600
    # The same number represented as words
    num_as_words = (
            "two hundred twenty two novemdecillion, " +
            "two hundred thirty two octodecillion, " +
            "two hundred forty four septdecillion, " +
            "six hundred twenty nine sexdecillion, " +
            "four hundred twenty quindecillion, " +
            "four hundred forty five quattuordecillion, " +
            "five hundred twenty nine tredecillion, " +
            "seven hundred thirty nine duodecillion, " +
            "eight hundred ninety three undecillion, " +
            "four hundred sixty one decillion, nine hundred nine nonillion, " +
            "nine hundred sixty seven octillion, two hundred six septillion, " +
            "six hundred sixty six sextillion, " +
            "nine hundred thirty nine quintillion, ninety six quadrillion, " +
            "four hundred ninety nine trillion, seven hundred sixty four billion, "
            + "nine hundred ninety million, nine hundred seventy nine thousand, " +
            "six hundred")
    assert ConvertNumbertoString().number_to_words(num) == num_as_words
