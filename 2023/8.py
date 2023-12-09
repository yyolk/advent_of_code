from collections import Counter
from typing import NamedTuple
from math import lcm


class Waypoint(NamedTuple):
    """Container for all the tuples of directions."""

    L: str
    R: str


def parse_input(serialized_input: str) -> (tuple["*str"], dict[str, Waypoint]):
    """Parse the serialized directions."""
    # Unpack the first line, skip the second, and set lines to the rest.
    instructive_direction, _, *lines = serialized_input.splitlines()[0:]
    result_map = {}
    for line in lines:
        key, value = line.split("=")
        result_map[key.strip()] = Waypoint(
            *[v.strip().lstrip("(").rstrip(")") for v in value.split(",")]
        )
    instructive_direction = tuple(instructive_direction)
    return instructive_direction, result_map


def navigate_result_map_1(
    instructive_directions, result_map: dict[str, Waypoint], starting_position="AAA"
) -> int:
    """Navigate the map given the navigation protocol and waypoints."""
    location = starting_position
    steps = 0
    while not location.endswith("Z"):
        for direction in instructive_directions:
            # Get the Waypoint.L or Waypoint.R
            location = getattr(result_map[location], direction)
            steps += 1
    return steps


def navigate_result_map_2(
    instructive_directions, result_map: dict[str, Waypoint]
) -> int:
    """Navigate the map with waypoints according the new set of instructions.

    Re-uses logic from the previous part, by calling it for each starting point.

    Lowest common multiple can determine when the waypoint cycles match up.
    """
    starting_points = [key for key in result_map.keys() if key.endswith("A")]
    all_steps = []
    for starting_point in starting_points:
        steps = navigate_result_map_1(
            instructive_directions, result_map, starting_point
        )
        all_steps.append(steps)
    # LCM will determine when their cycles meet.
    return lcm(*all_steps)


with open("8.txt") as fp:
    puzzle_input = fp.read()
    print(navigate_result_map_1(*parse_input(puzzle_input)))
    print(navigate_result_map_2(*parse_input(puzzle_input)))
