import re

from collections import defaultdict


next_disabled_pattern = re.compile("#")


def get_next_disabled(springs: str, search_start: int) -> int:
    if match_ := next_disabled_pattern.search(springs, search_start):
        return match_.start()
    return len(springs)


def get_positions(springs: str, group: int) -> list[tuple[int, int]]:
    pattern = f"(?<!#)(?=[?#]{{{group}}}(?!#))"
    return [(m.start(), m.start() + group) for m in re.finditer(pattern, springs)]


def count_possibilities(springs: str, groups: list[int]) -> int:
    counts = {(-1, -1): 1}
    for group in groups:
        new_counts = defaultdict(int)
        positions = get_positions(springs, group)
        for (prev_start, prev_end), count in counts.items():
            next_disabled = get_next_disabled(springs, prev_end + 1)
            for curr_start, curr_end in positions:
                if curr_start <= prev_end:
                    continue
                if curr_start > next_disabled:
                    break
                new_counts[curr_start, curr_end] += count
        counts = new_counts
    return sum(count for (_, end), count in counts.items() if "#" not in springs[end:])


def parse_spring_field_1(serialized_input: str) -> list[tuple[str, list[int]]]:
    return [
        (springs, list(map(int, groups.split(","))))
        for springs, groups in [line.split() for line in serialized_input.splitlines()]
    ]


def parse_spring_field_2(serialized_input: str) -> list[tuple[str, list[int]]]:
    return [
        ("?".join(springs for _ in range(5)), groups * 5)
        for springs, groups in parse_spring_field_1(serialized_input)
    ]


def sum_possibilities(parsed_spring_field) -> int:
    return sum(
        count_possibilities(springs, groups) for springs, groups in parsed_spring_field
    )


with open("12.txt") as fp:
    puzzle_input = fp.read()
    print(sum_possibilities(parse_spring_field_1(puzzle_input)))
    print(sum_possibilities(parse_spring_field_2(puzzle_input)))
