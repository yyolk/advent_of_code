from typing import Callable, Iterator


def get_difflist(numbers: list[int]) -> Iterator[list[int]]:
    # The first row in our calculation is the same as the input.
    yield numbers
    # Copy numbers into diffs.
    diffs = numbers
    # Determine if diffs is now all zeroes.
    while not all([diff == 0 for diff in diffs]):
        newdiffs = []
        for i in range(1, len(diffs)):
            newdiffs.append(diffs[i] - diffs[i - 1])
        diffs = newdiffs
        # Yield this row of differences, which may or not be all zeroes.
        yield diffs


def extrapolate_next_number_1(numbers: list[int]) -> int:
    """Part 1."""
    difflist = get_difflist(numbers)
    return sum(diffs[-1] for diffs in difflist)


def extrapolate_next_number_2(numbers: list[int]) -> int:
    """Part 2."""
    difflist = list(get_difflist(numbers))
    next_number = 0
    for diffs in reversed(difflist):
        next_number = diffs[0] - next_number
    return next_number


def deserialize_and_summate(
    serialized_input: str, extrapolation_function: Callable[[list[int]], int]
) -> int:
    """Unpacks the serialized input and summates the results from each part's solution."""
    return sum(
        extrapolation_function(list(map(int, line.split())))
        for line in serialized_input.splitlines()
    )


with open("9.txt") as fp:
    puzzle_input = fp.read()
    print(deserialize_and_summate(puzzle_input, extrapolate_next_number_1))
    print(deserialize_and_summate(puzzle_input, extrapolate_next_number_2))
