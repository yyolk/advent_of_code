from collections import Counter


# Programmatic creation of types ranking using example hands from prompt.
types = [
    "".join(map(str, n))
    for n in [
        sorted(c)
        for c in [
            Counter(s).values()
            # Use the example literals for calculating representation of all hand types.
            for s in ["23456", "A23A4", "23432", "TTT98", "23332", "AA8AA", "AAAAA"]
        ]
    ]
][::-1]

# Literal result:
# types = ["5", "14", "23", "113", "122", "1112", "11111"]


def update_hand_type(hands: dict, jokers_wild=False) -> dict:
    for hand in hands:
        hand_counter = Counter(hand)

        if "J" in hand_counter and hand != "JJJJJ" and jokers_wild:
            next_joker = hand_counter.pop("J")
            hand_counter[hand_counter.most_common(1)[0][0]] += next_joker

        type_ = "".join(sorted(list(str(n) for n in hand_counter.values())))
        hands[hand]["type"] = type_

    return hands


def calculate_winnings(hands: dict, J=11) -> int:
    """Calculate the total winnings given all hands."""
    cards = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": J,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    rank = 1
    total_winnings = 0
    for type_ in reversed(types):
        this_types_hands = [
            key for key, value in hands.items() if value["type"] == type_
        ]
        if this_types_hands:
            this_types_hands = sorted(
                this_types_hands, key=lambda x: [cards[card] for card in x]
            )
        for hand in this_types_hands:
            total_winnings += rank * hands[hand]["bet"]
            rank += 1

    return total_winnings


def parse_hands(serialized_input: str) -> dict:
    hands = {}
    for hand in serialized_input.splitlines():
        hands[hand.split()[0]] = dict(bet=int(hand.split()[1]))
    return hands


with open("7.txt") as fp:
    puzzle_input = fp.read()
    print(calculate_winnings(update_hand_type(parse_hands(puzzle_input))))
    print(
        calculate_winnings(update_hand_type(parse_hands(puzzle_input), jokers_wild=True), J=0)
    )
