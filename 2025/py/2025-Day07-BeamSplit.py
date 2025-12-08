from dataclasses import dataclass


@dataclass(frozen=True)
class Input:
    splitters: set[tuple[int, int]]
    start: tuple[int, int]
    nr: int
    nc: int

def read_input(file_path: str) -> Input:
    splitters = []
    with open(file_path, "r") as file:
        for ri, row in enumerate(file.readlines()):
            for ci, col in enumerate(row):
                if col == "S":
                    start = (ri, ci)
                elif col == "^":
                    splitters.append((ri, ci))
    return Input(splitters=set(splitters), start=start, nr=ri+1, nc=ci+1)

def part1(input: Input) -> int:
    rowi = input.start[0]
    beams = set([input.start])
    split_count = 0
    while(rowi < input.nr):
        beams_next = set()
        for beam in beams:
            if (beam[0] + 1, beam[1]) in input.splitters:
                split_count += 1
                beams_next.add((beam[0] + 1, beam[1]-1))
                beams_next.add((beam[0] + 1, beam[1]+1))
            else:
                beams_next.add((beam[0] + 1, beam[1]))
        beams = beams_next
        rowi += 1
    return split_count

def part2(input: Input) -> int:
    cache = {}
    def count_worlds(pos: tuple[int, int]) -> int:
        if pos in cache:
            return cache[pos]
        if pos[0] == input.nr:
            return 1
        result = 0
        if (pos[0]+1, pos[1]) in input.splitters:
            result += count_worlds((pos[0]+1, pos[1]-1))
            result += count_worlds((pos[0]+1, pos[1]+1))
        else:
            result += count_worlds((pos[0]+1, pos[1]))
        cache[pos] = result
        return result
    return count_worlds(input.start)

def main():
    input_main = read_input("2025-Day07.txt")
    input_test = read_input("2025-Day07-test.txt")
    print("part 1 test", part1(input_test))
    # 21
    print("part 1 main", part1(input_main))
    # 0

    print("part 2 test", part2(input_test))
    # 40
    print("part 2 main", part2(input_main))
    # 422102272495018

if __name__ == "__main__":
    main()