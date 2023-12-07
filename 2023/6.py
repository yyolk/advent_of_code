from functools import reduce


def ways_to_win(race_time, race_record):
    speed = 0
    charge_time = 0
    distance = 0
    ways_to_win = []
    midpoint = race_time // 2
    for i in range(race_time, 0, -1):
        speed = charge_time = race_time - i
        distance = speed * (race_time - charge_time)
        if distance > race_record:
            ways_to_win.append(distance)
        # Exit early if we've passed the optimal charge ranges,
        # and now we're seeing smaller than the reocrd results.
        elif i < midpoint:
            break

    return ways_to_win


def margin_of_error_1(serialized_sheet: str) -> int:
    times, distances = serialized_sheet.splitlines()
    _, times = times.split(":")
    times = map(int, times.split())
    _, distances = distances.split(":")
    distances = map(int, distances.split())
    all_races_winning_possibilies = []
    for td in zip(times, distances):
        all_races_winning_possibilies.append(len(ways_to_win(*td)))
    return reduce(lambda x, y: x * y, all_races_winning_possibilies)


def margin_of_error_2(serialized_sheet: str) -> int:
    time_, distance = serialized_sheet.splitlines()
    time_ = int("".join(time_.split(":")[1].split()))
    distance = int("".join(distance.split(":")[1].split()))
    return len(ways_to_win(time_, distance))


with open("6.txt") as fp:
    puzzle_input = fp.read()
    print(margin_of_error_1(puzzle_input))
    print(margin_of_error_2(puzzle_input))
