import re


PART_NUMBER_PATTERN = re.compile(r"\d+")


def parse_schematic_1(serialized_schematic: str) -> int:
    # Initialize the sum of part numbers.
    sum_part_numbers = 0
    # Split the serialized schematic into lines.
    lines = serialized_schematic.splitlines()
    # Get the number of lines.
    n = len(lines)

    # Iterate through each line in the schematic.
    for x in range(n):
        for number_match in PART_NUMBER_PATTERN.finditer(lines[x]):
            # Initialize part_number to -1, so we don't add the same match.
            part_number = -1
            # Work within the range of the found number.
            for y in range(*number_match.span()):
                # Iterate over positions around the number.
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # Check if the position is within schematic bounds and contains
                        # a non-digit and non-period character.
                        if (
                            0 <= x + i < n
                            and 0 <= y + j < n
                            and not lines[x + i][y + j].isdigit()
                            and lines[x + i][y + j] != "."
                        ):
                            # If part_number has not been assigned this round, assign
                            # it to the current number_match, this also deduplicates.
                            if part_number == -1:
                                part_number = int(number_match.group())
                            # Break the inner loop if a valid adjacent character is found.
                            break
            # Add the part_number to the sum if it is non-negative.
            sum_part_numbers += part_number if part_number >= 0 else 0
    # Return the final sum of part numbers.
    return sum_part_numbers


def parse_schematic_2(serialized_schematic: str) -> int:
    # sum_part_numbers = 0
    lines = serialized_schematic.splitlines()
    n = len(lines)
    # Create a multi-dimensional array for storing numbers that are adjacent to "*".
    adjacent_numbers = [[[] for x in range(n)] for x in range(n)]
    for x in range(n):
        # Find all occurrences of numbers in the line.
        for number_match in PART_NUMBER_PATTERN.finditer(lines[x]):
            # Work within the range of the found number.
            for y in range(*number_match.span()):
                # Iterate over the positions around the number.
                for i in range(-1, 2):
                    for j in range(
                        -1 if y == number_match.span()[0] else 0,
                        1 if y < number_match.span()[1] - 1 else 2,
                    ):
                        # Check if the position is within the schematic bounds and
                        # contains a "*".
                        if (
                            0 <= x + i < n
                            and 0 <= y + j < n
                            and lines[x + i][y + j] == "*"
                        ):
                            # Append the current number to the adjacent position.
                            adjacent_numbers[x + i][y + j].append(
                                int(number_match.group())
                            )

    # Calculate the sum of products for pairs of adjacent numbers.
    return sum(
        adjacent_numbers[x][y][0] * adjacent_numbers[x][y][1]
        for x in range(n)
        for y in range(n)
        if len(adjacent_numbers[x][y]) == 2
    )


with open("3.txt") as fp:
    puzzle_input = fp.read()
    print(parse_schematic_1(puzzle_input))
    print(parse_schematic_2(puzzle_input))
