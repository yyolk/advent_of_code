import regex


def find_calibration(scrambled_input: str) -> int:
    """Part 1"""
    lines = scrambled_input.splitlines()
    total = 0
    for line in lines:
        digits = ""
        # Get the first digit from the left
        for c in line:
            if c.isdigit():
                digits = c
                break
        # Get the first digit from the right.
        for c in line[::-1]:
            if c.isdigit():
                digits += c
                break
        # Add the digits to the running total.
        total += int(digits)
    return total


numbers_to_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

find_string_digit_pattern = re.compile("|".join(numbers_to_digits.keys()))


def find_calibration2(scrambled_input: str) -> int:
    """Part 2"""
    total = 0
    lines = scrambled_input.splitlines()
    for line in lines:
        digits = ""
        # `overlapped=True` from regex module is required,
        # input is sometimes like "oneeight" or "twoone"
        matches = [
            m for m in regex.finditer(find_string_digit_pattern, line, overlapped=True)
        ]
        # Starting from the left, get all matches of digits and matches of words,
        # including overlapped, in the right sequence.
        for idx, c in enumerate(line):
            if c.isdigit():
                digits += c
                continue
            for m in matches:
                # We want to count each found number as word once,
                # we can do that when idx equals the start of the match.
                if m.start(0) == idx:
                    digits += numbers_to_digits[m.group()]
        # Add just the left-most and right-most found digit
        total += int(digits[0] + digits[-1])
    return total


with open("1.txt") as fp:
    puzzle_input = fp.read()
    print(find_calibration(puzzle_input))
    print(find_calibration2(puzzle_input))
