def map_seeds_1(serialized_almanac: str) -> int:
    """Exhaustive approach :P"""

    def get_seeds(serialized_almanac: str) -> list[int]:
        """Extract seeds from the serialized almanac."""
        first_line = serialized_almanac.splitlines()[0].strip()
        seeds = list(map(int, first_line.split()[1:]))
        return seeds

    def get_maps(serialized_almanac: str) -> list[tuple[int]]:
        """Extract almanac and maps from the serialized almanac."""
        lines = serialized_almanac.split("\n\n")[1:]
        almanac = {}
        x_ref = {}
        for line in lines:
            key, value = line.split(":")[0].split("-to-")
            x_ref[key] = value
            values = [
                tuple(map(int, (dest, source, length)))
                for dest, source, length in [
                    l.split() for l in line.split(":")[1].split("\n")[1:]
                ]
            ]
            almanac[key] = values
        only_maps = list(
            filter(
                lambda l: l[0].isdigit() if l else None,
                serialized_almanac.splitlines()[1:],
            )
        )
        maps = [
            tuple(map(int, (dest, source, length)))
            for dest, source, length in [m.split() for m in only_maps]
        ]
        return almanac, maps

    def convert_number(source, dest, length, number):
        """Convert a number through a given map."""
        if source <= number <= (source + length):
            return dest + (number - source)
        else:
            return False

    def convert_through_maps(maps, number):
        """Convert a number through a series of maps."""
        for dest, source, length in maps:
            num = convert_number(source, dest, length, number)
            if num:
                break
        else:
            num = number
        return num

    # Extract seeds, almanac, and maps
    seeds = get_seeds(serialized_almanac)
    almanac, _ = get_maps(serialized_almanac)
    # The exhaustive approach ;P
    return min(
        [
            convert_through_maps(
                almanac["humidity"],
                convert_through_maps(
                    almanac["temperature"],
                    convert_through_maps(
                        almanac["light"],
                        convert_through_maps(
                            almanac["water"],
                            convert_through_maps(
                                almanac["fertilizer"],
                                convert_through_maps(
                                    almanac["soil"],
                                    convert_through_maps(almanac["seed"], seed),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            for seed in seeds
        ]
    )


def map_seeds_2(serialized_almanac: str) -> int:
    # Split the input almanac into seeds and maps
    input_almanac_split = serialized_almanac.split("\n\n")
    seeds = [int(n) for n in input_almanac_split[0].split(":")[1].split()]
    maps = [
        [[int(m) for m in n.split()] for n in l.split(":\n")[1].splitlines()]
        for l in input_almanac_split[1:]
    ]
    maps_depth = len(maps) - 1

    # Initialize map_ranges with empty lists for each depth
    map_ranges = [[] for _ in range(maps_depth + 1)]

    # Populate map_ranges with map information
    for depth, map_ in enumerate(maps):
        for destination_start, source_start, length in map_:
            map_ranges[depth].append(
                [source_start, source_start + length, destination_start]
            )

    def map_seed_range(depth, seed_start, seed_end):
        """Inner function to recursively map seed ranges through different maps."""
        for source_start, source_end, destination_start in map_ranges[depth]:
            if source_start <= seed_start < source_end:
                if seed_end < source_end:
                    # Calculate new seed range based on the map
                    new_seed_start, new_seed_end = (
                        seed_start - source_start + destination_start,
                        seed_end - source_start + destination_start,
                    )
                    # Recursively map the new seed range
                    return (
                        new_seed_start
                        if depth == maps_depth
                        else map_seed_range(depth + 1, new_seed_start, new_seed_end)
                    )
                else:
                    # Handle case where seed range extends beyond the current map
                    return min(
                        map_seed_range(depth, seed_start, source_end - 1),
                        map_seed_range(depth, source_end, seed_end),
                    )
        # Base case: return seed values if depth is the last map depth
        return (
            seed_start
            if depth == maps_depth
            else map_seed_range(depth + 1, seed_start, seed_end)
        )

    # Find the minimum mapped seed value for each seed pair
    return min(
        [
            map_seed_range(0, seeds[i], seeds[i] + seeds[i + 1])
            for i in range(0, len(seeds), 2)
        ]
    )


with open("5.txt") as fp:
    puzzle_input = fp.read()
    print(map_seeds_1(puzzle_input))
    print(map_seeds_2(puzzle_input))
