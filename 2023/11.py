def parse_cosmos(
    serialized_cosmos: str, expansion: int = 2
) -> (list[tuple[int, int]], int):
    """Part 1 & Part 2.

    Parse the serialized cosmos string.
    Find all galaxies and calculate the result.

    Args:
        serialized_cosmos: The input string to deserialize.
        expansion: The rate of expansion for this cosmos.

    Returns:
        galaxies: The position of the galaxies after computing expansion.
        result: The sum of the shortest distance between each pair of galaxies.
    """
    galaxies = [
        (x, y)
        for y, line in enumerate(serialized_cosmos.splitlines())
        for x, galaxy in enumerate(line)
        if galaxy == "#"
    ]
    width = max(galaxies, key=lambda g: g[0])[0] + 1
    height = max(galaxies, key=lambda g: g[1])[1] + 1
    columns = [expansion - 1] * width
    rows = [expansion - 1] * height
    for galaxy in galaxies:
        columns[galaxy[0]] = 0
        rows[galaxy[1]] = 0
    columns = [sum(columns[: i + 1]) for i in range(len(columns))]
    rows = [sum(rows[: i + 1]) for i in range(len(rows))]
    galaxies = [(x + columns[x], y + rows[y]) for x, y in galaxies]
    result = sum(
        abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
        for i in range(len(galaxies))
        for j in range(i + 1, len(galaxies))
    )
    return galaxies, result


def create_cosmos_drawing(galaxies: list[tuple[int, int]], expansion: int = 2) -> str:
    """Draw the expanded cosmos given all the galaxies locations.

    For comparing the prompt example into the expanded example, but works on any input.

    Args:
        galaxies: A list of x,y coordinates of all the galaxies (in their expanded position).
        expansion: The rate of the expansion for filling in the empty space.

    Returns:
        A string that represents the cosmos as a drawing of "." for empty space and "#"
        for space occupied by a galaxy.
    """
    lines = []
    for y in range(max(galaxies, key=lambda g: g[1])[1] + (expansion - 1)):
        line = ""
        for x in range(max(galaxies, key=lambda g: g[0])[0] + (expansion - 1)):
            if (x, y) in galaxies:
                line += "#"
            else:
                line += "."

        lines.append(line)
    drawing = "\n".join(lines)
    return drawing


with open("11.txt") as fp:
    puzzle_input = fp.read()
    print(parse_cosmos(puzzle_input)[1])
    print(parse_cosmos(puzzle_input, 1_000_000)[1])
