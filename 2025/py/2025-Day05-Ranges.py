from dataclasses import dataclass

@dataclass(frozen=True)
class Range:
    start: int
    end: int

@dataclass(frozen=True)
class Input:
    ranges: list[Range]
    values: list[int]

def read_input(file_path: str) -> list[Range]:
    with open(file_path) as file:
        mode = "ranges"
        ranges = []
        values = []
        for line in file.readlines():
            if line.strip() == "":
                mode = "values"
                continue
            if mode == "ranges":
                ranges.append(Range(start=int(line.split("-")[0]), end=int(line.split("-")[1])))
            elif mode == "values":
                values.append(int(line.strip()))
    return Input(ranges=ranges, values=values)

def part1(input: Input) -> int:
    fresh = 0
    for val in input.values:
        is_fresh = False
        for range in input.ranges:
            if val >= range.start and val <= range.end:
                is_fresh = True
                break
        if is_fresh:
            fresh += 1
    return fresh

def part2(input: Input) -> int:
    events = []
    OPEN = 0 # when sorting, process open events first
    CLOSE = 1
    valid_range = 0
    for range in input.ranges:
        events.append((range.start, OPEN))
        events.append((range.end, CLOSE))
    events.sort()
    opened_at = 0
    current_count = 0
    for event in events:
        if event[1] == OPEN:
            if current_count == 0:
                opened_at = event[0]
            current_count += 1
        else: # event[1] == CLOSE
            current_count -= 1
            if current_count == 0:
                valid_range += event[0] - opened_at + 1
    return valid_range

def main():
    test_input = read_input("2025-Day05-test.txt")
    main_input = read_input("2025-Day05.txt")
    print("part 1 test", part1(test_input))
    # 3
    print("part 1 main", part1(main_input))
    # 513

    print("part 2 test", part2(test_input))
    # 14
    print("part 2 main", part2(main_input))
    # 339668510830757

if __name__ == "__main__":
    main()