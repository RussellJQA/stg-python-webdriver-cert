"""
The ConvertIntegerToWords utility class is used to convert an integer (e.g., 990979600)
to its corresponding string of words
(e.g., 'nine hundred ninety million, nine hundred seventy nine thousand six hundred')
"""

# Custom imports
from services.integer_triad_to_words import ConvertIntegerTriadToWords


class ConvertIntegerToWords:

    @staticmethod
    def get_grouping_separator(triad: str, triad_group_number: int,
                               triad_count: int) -> str:

        if triad_group_number:
            if int(triad) >= 100 or triad_group_number < triad_count - 1:
                return ", "
            else:
                return " "
        else:
            return ""

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
                    triad_as_string = ConvertIntegerTriadToWords().triad_to_string(
                        int(triad))
                    triad_grouping = TRIAD_GROUPINGS[triad_count -
                                                     triad_group_number -
                                                     1]  # 6: "quintillion",

                    grouping_separator = ConvertIntegerToWords(
                    ).get_grouping_separator(triad, triad_group_number,
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
    if ConvertIntegerToWords().number_to_words(num) != num_as_words:
        raise ValueError
