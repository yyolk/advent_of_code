def total_scratch_cards_1(serialized_table: str) -> int:
    # Split the serialized table into lines.
    lines = serialized_table.splitlines()
    # Initialize the list to store the number of matches for each card.
    matches = []

    # Iterate through each line in the table.
    for line in lines:
        # Split the line into card numbers and winning/player numbers.
        _, numbers = line.split(":")
        winning_numbers, player_numbers = numbers.split("|")

        # Convert winning and player numbers into sets of integers.
        winning_numbers = set(map(int, winning_numbers.strip().split()))
        player_numbers = set(map(int, player_numbers.strip().split()))

        # Calculate the number of matching numbers between winning and player numbers.
        matches.append(len(player_numbers & winning_numbers))

    # Calculate the total points based on the number of matches for each card with the
    # rules of doubling after the first win.
    return sum(int(2 ** (m - 1)) for m in matches)


def total_scratch_cards_2(serialized_table: str) -> int:
    # Split the serialized table into lines.
    lines = serialized_table.splitlines()

    # Initialize a list to store the number of matches for each card.
    matches = []

    # Iterate through each line in the serialized table.
    for i in range(len(lines)):
        # Split the line into card numbers and winning/player numbers.
        _, numbers = lines[i].split(":")
        winning_numbers, player_numbers = numbers.split("|")

        # Convert winning and player numbers into sets of integers.
        winning_numbers = set(map(int, winning_numbers.strip().split()))
        player_numbers = set(map(int, player_numbers.strip().split()))

        # Calculate the number of matching numbers between winning and player numbers.
        matches.append(len(winning_numbers & player_numbers))

    # Initialize a list to track instances of each scratchcard.
    scratchcards_instances = [1] * len(matches)

    # Iterate through each card and update the instances based on the points from matches.
    for i, match_ in enumerate(matches):
        for j in range(i + 1, i + match_ + 1):
            scratchcards_instances[j] += scratchcards_instances[i]

    # Calculate the total number of scratchcards won.
    return sum(scratchcards_instances)


with open("4.txt") as fp:
    puzzle_input = fp.read()
    print(total_scratch_cards_1(puzzle_input))
    print(total_scratch_cards_2(puzzle_input))
