from dataclasses import dataclass

@dataclass(frozen=True)
class Range:
    start: str
    end: str

def import_data(file_path: str) -> list[Range]:
    output = []
    for line in open(file_path).readlines():
        for part in line.strip().split(","):
            if not part:
                continue
            start, end = part.split("-")
            output.append(Range(start=start, end=end))
    return output

def find_half_dups(input: Range) -> list[int]:
    if len(input.start) > len(input.end):
        return []
    if len(input.start) == len(input.end):
        if len(input.start) % 2 == 1:
            return []
        half_size = len(input.start) // 2

        begin_first_half = int(input.start[:half_size])
        begin_last_half = int(input.start[half_size:])
        begin = begin_first_half if begin_first_half >= begin_last_half else begin_first_half+1

        end_first_half = int(input.end[:half_size])
        end_last_half = int(input.end[half_size:])
        end = end_first_half if end_first_half <= end_last_half else end_first_half-1

        if begin <= end:
            return list(int(str(x) * 2) for x in range(begin, end+1))
        else:
            return []
    # len(range.start) < len(range.end)
    return (
        find_half_dups(Range(start=input.start, end="9" * len(input.start)))
        + find_half_dups(Range(start="1" + ("0" * (len(input.end) - 1)), end=input.end))
    )

def find_size_dups(input: Range, size: int) -> list[int]:
    if len(input.start) > len(input.end):
        return []
    if len(input.start) == len(input.end):
        if len(input.start) < 2:
            return []
        if len(input.start) % size != 0:
            return []
        
        begin_parts = [int(input.start[i:i+size]) for i in range(0, len(input.start), size)]
        end_parts = [int(input.end[i:i+size]) for i in range(0, len(input.end), size)]

        begin = begin_parts[0]
        for other in begin_parts[1:]:
            if other < begin:
                break
            elif other > begin:
                begin = begin + 1
                break

        end = end_parts[0]
        for other in end_parts[1:]:
            if other < end:
                end = end - 1
                break
            elif other > end:
                break

        if begin <= end:
            return list(int(str(x) * len(begin_parts)) for x in range(begin, end+1))
        else:
            return []
    # len(range.start) < len(range.end)
    return (
        find_size_dups(Range(start=input.start, end="9" * len(input.start)), size)
        + find_size_dups(Range(start="1" + ("0" * (len(input.end) - 1)), end=input.end), size)
    )

def score_range(input: Range) -> int:
    return sum(find_half_dups(input))

def part1(data: list[Range]) -> int:
    return sum(score_range(range) for range in data)

def part2(data: list[Range]) -> int:
    bad_ids = set()
    for input in data:
        max_size = max(len(input.start), len(input.end)) // 2
        dups = []
        for size in range(1, max_size + 1):
            dups += find_size_dups(input, size)
        bad_ids.update(dups)
    return sum(bad_ids)

def main():
    test_data = import_data("2025-Day02-test.txt")
    main_data = import_data("2025-Day02.txt")
    print("part 1 test", part1(test_data))
    # 1227775554
    print("part 1 main", part1(main_data))
    # 30323879646

    print("part 2 test", part2(test_data))
    # 4174379265
    print("part 2 main", part2(main_data))
    # too high: 43872176459 had some number outside of range (bad end calc)
    # too high: 43872163599  was failing on Range(start='3', end='16')
    # 43872163557


if __name__ == "__main__":
    main()