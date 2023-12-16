# Thanks to https://github.com/derailed-dash/Advent-of-Code/blob/526a76bf8187c09ae1b53d0129a5ac6b5852c6b7/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
# for the help on part 2
from dataclasses import dataclass, field


def calculate_hash(step: str) -> int:
    current_value = 0
    for char in step:
        # Get the ascii value
        current_value += ord(char)
        # Multiply by 17
        current_value *= 17
        # Set the current_value to modulo 256
        current_value %= 256
    return current_value


def part_1(serialized_instructions: str):
    """Part 1."""
    steps = serialized_instructions.split(",")

    all_hashes = [calculate_hash(step) for step in steps]
    return sum(all_hashes)


@dataclass
class Box:
    num: int
    lenses: list[tuple[str, int]] = field(default_factory=list)
    lenses_set: set[str] = field(default_factory=set)

    def focusing_power(self) -> int:
        """Determine the focussing power of this box.

        As calculated as sum over all lenses of:
            box_num (1-indexed) * slot-num (1-indexed) * lens focal length

        """
        pwr = 0
        for slot, lens in enumerate(self.lenses):
            pwr += (self.num + 1) * (slot + 1) * lens[1]

        return pwr

    def pop_lens(self, label: str) -> tuple[str, int] | None:
        """Pop the lens with the specified label. If the lens exists, return (location, lens)"""
        if label in self.lenses_set:
            self.lenses_set.remove(label)
            return self.lenses.pop(self.get_lens_location(label))

        return None

    def get_lens_location(self, label: str) -> int:
        for idx, (curr_label, curr_pwr) in enumerate(self.lenses):
            if label == curr_label:
                return idx

        raise KeyError("Lens not found")

    def add_lens(self, label: str, f_length: int, location: int | None = None):
        """Add a lens at the specified location, or at the end."""
        lens = (label, f_length)
        assert label not in self.lenses_set, "There should be no lens with this label."
        self.lenses_set.add(label)
        if location is not None:
            self.lenses.insert(location, lens)
        else:
            self.lenses.append(lens)


def part_2(serialized_instructions: str) -> int:
    """Part 2."""
    steps = serialized_instructions.split(",")
    boxes = {box_num: Box(box_num) for box_num in range(256)}

    for step in steps:
        operation = "=" if "=" in step else "-"
        lens_label = step.split(operation)[0]
        curr_box = boxes[calculate_hash(lens_label)]
        # Remove lens.
        if operation == "-":
            curr_box.pop_lens(lens_label)
        else:
            f_length = int(step[-1])
            location = None
            if lens_label in curr_box.lenses_set:
                location = curr_box.get_lens_location(lens_label)
                curr_box.pop_lens(lens_label)

            curr_box.add_lens(lens_label, f_length, location)

    return sum(box.focusing_power() for box in boxes.values())


with open("15.txt") as fp:
    puzzle_input = fp.read()
    print(part_1(puzzle_input))
    print(part_2(puzzle_input))
