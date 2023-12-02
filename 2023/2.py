from functools import reduce


def _parse_games(sinput: str) -> dict[int, list[Counter]]:
    """Deserialize our input."""
    parsed_games = {}
    for line in sinput.splitlines():
        # Extract the game_number from the header.
        game_number_match = re.search(r"Game (\d+):", line)
        game_number = game_number_match.group(1)
        # Do a rough strip and split of all the components for each round.
        cube_picks_raw = [
            # Remove whitespace and split on ",".
            [unclean.strip() for unclean in round_.split(",")]
            # Separate each round that is present after the header with ';'.
            for round_ in line[game_number_match.end(0) :].split(";")
        ]
        # Initialize sanitized cube_picks, which are rounds for this game.
        cube_picks = []
        for pick in cube_picks_raw:
            # Initialize empty counter for the expected colors
            c = Counter({"red": 0, "green": 0, "blue": 0})
            for item in pick:
                # Every pick is a "number color".
                num, color = item.split()
                c[color] += int(num)
            cube_picks.append(c)
        # Assign these rounds to our parsed_games dict with the game_number as key.
        parsed_games[int(game_number)] = cube_picks
    return parsed_games


def part1(sinput: str, bag_count: Counter) -> int:
    """Part 1"""
    parsed_games = _parse_games(sinput)
    total = 0
    valid_game_numbers = []
    for game_number, rounds in parsed_games.items():
        valid_rounds = []
        for round_ in rounds:
            # If round_ is a sub-multiset of the bag_count, it was valid.
            if round_ <= bag_count:
                valid_rounds.append(True)
            else:
                valid_rounds.append(False)
        # If the game had all valid rounds, it was a valid game.
        if all(valid_rounds):
            # Our total is an ongoing sum of the valid game numbers
            total += game_number
            valid_game_numbers.append(game_number)
    return total


def part2(sinput: str) -> int:
    parsed_games = _parse_games(sinput)
    total = 0
    for games in parsed_games.values():
        min_cube = Counter({"green": 0, "red": 0, "blue": 0})
        # Work through all the rounds to determine the minimum amount of cubes needed
        # for each color for the game to work, by finding the max value for each color.
        for round_ in games:
            for color, number in round_.items():
                min_cube[color] = max(number, min_cube[color])
        cube_power = reduce(lambda x, y: x * y, min_cube.values())
        # Our total is an ongoing sum of the product of all color counts.
        total += cube_power
    return total


with open("2.txt") as fp:
    puzzle_input = fp.read()
    # Given known_bag_contents
    known_bag_contents = Counter({"red": 12, "green": 13, "blue": 14})
    print(part1(puzzle_input, known_bag_contents))
    print(part2(puzzle_input))
