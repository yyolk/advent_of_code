import numpy as np


def parse_rocks(serialized_rocks: str) -> np.ndarray:
    """Convert the rocks input into a numpy.ndarray."""
    return np.array([list(row) for row in serialized_rocks.splitlines()])


def tilt_north(rocks: np.ndarray) -> np.ndarray:
    highest_occupied = {col_num: -1 for col_num, _ in enumerate(rocks[0])}

    for row_num, row in enumerate(rocks):
        for col_num, val in enumerate(row):
            # Roll this rock up to the highest occupied + 1.
            if val == "O":
                target_row = highest_occupied[col_num] + 1
                # We need to move this rock, otherwise it is blocked.
                if target_row != row_num:
                    rocks[target_row, col_num] = "O"
                    rocks[row_num, col_num] = "."
                    highest_occupied[col_num] = target_row

            if rocks[row_num, col_num] != ".":
                highest_occupied[col_num] = row_num

    return rocks


def part_1(rocks: np.ndarray) -> int:
    """Part 1."""
    rocks = tilt_north(rocks)
    row_counts = np.sum(rocks == "O", axis=1)
    total_load = sum(
        (rocks.shape[0] - row) * val for (row, val) in enumerate(row_counts)
    )
    return total_load


def tilt_rocks_cycle(rocks: np.ndarray) -> np.ndarray:
    """Part 2 requirement."""
    for _ in range(4):
        rocks = tilt_north(rocks)
        # Rotate clockwise
        rocks = np.rot90(rocks, -1)
    return rocks


def part_2(rocks: np.ndarray) -> int:
    """Part2."""
    required_cycles = 1_000_000_000
    repeat_length = 1

    rocks_cache = {}
    for i in range(required_cycles):
        rocks = tilt_rocks_cycle(rocks)

        # Cache the rocks as tuple
        rocks_top = tuple(map(tuple, rocks))
        if rocks_top in rocks_cache:
            prev_iteration = rocks_cache[rocks_top]
            repeat_length = i - prev_iteration
            break

        rocks_cache[rocks_top] = i

    remaining_cycles = required_cycles - (i + 1)
    additional_cycles = remaining_cycles % repeat_length

    for i in range(additional_cycles):
        rocks = tilt_rocks_cycle(rocks)

    row_counts = np.sum(rocks == "O", axis=1)
    total_load = sum(
        (rocks.shape[0] - row) * val for (row, val) in enumerate(row_counts)
    )

    return total_load


with open("14.txt") as fp:
    puzzle_input = fp.read()
    print(part_1(parse_rocks(puzzle_input)))
    print(part_2(parse_rocks(puzzle_input)))
