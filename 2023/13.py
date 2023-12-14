from functools import partial

import numpy as np


def deserialize_notes(serialized_notes: str) -> list[np.ndarray]:
    """Deserialize the serialized notes.

    Args:
        serialized_notes: The serialized field notes.

    Returns:
        A list of numpy arrays representing all patterns from the notes.
    """

    def parse_pattern(pattern: str):
        """Inner function for converting "#" and "." into a numpy.ndarray.

        Args:
            pattern: A full pattern from the serialized notes.

        Returns:
            Converts "#" and "." into True and False respectively.
        """
        return np.array([[x == "#" for x in line] for line in pattern.splitlines()])

    return [parse_pattern(pattern) for pattern in serialized_notes.split("\n\n")]


def score_pattern(pattern: np.ndarray, diff: int = 0) -> int:
    """The primary method for finding our solution.

    Args:
        pattern: The deserialized pattern to score.

    Returns:
        The score for the pattern.
    """
    # Get the dimensions (height and width) of the input pattern.
    height, width = pattern.shape

    # Check for differences along the columns.
    for i in range(1, width):
        m = min(i, width - i)
        # XOR (^) operation on subarrays of the pattern along the columns.
        if (np.fliplr(pattern[:, i - m : i]) ^ pattern[:, i : i + m]).sum() == diff:
            # Count columns to the left.
            return i

    # Check for differences along the rows.
    for i in range(1, height):
        m = min(i, height - i)
        # XOR (^) operation on subarrays of the pattern along the rows.
        if (np.flipud(pattern[i - m : i, :]) ^ pattern[i : i + m, :]).sum() == diff:
            # Count rows above and multiply it by 100.
            return i * 100


def part_1(serialized_notes: str) -> int:
    """Part 1."""
    patterns = deserialize_notes(serialized_notes)
    return sum(map(score_pattern, patterns))


def part_2(serialized_notes: str) -> int:
    """Part 2.

    There's an expected difference of 1 due to the smudge which should be the
    opposite value.
    """
    patterns = deserialize_notes(serialized_notes)
    return sum(map(partial(score_pattern, diff=1), patterns))


with open("13.txt") as fp:
    puzzle_input = fp.read()
    print(part_1(puzzle_input))
    print(part_2(puzzle_input))
