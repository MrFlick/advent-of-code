from typing import List, Tuple

Coord = Tuple[int, int]

def get_input(path, expand_factor=2) -> List[Coord]:
    galaxies = []
    col_empty = []
    ncol = 0
    r = 0
    with open(path) as f:
        for line in f:
            row_empty = True
            if ncol == 0:
                ncol = len(line)-1
                col_empty = [True for _ in range(ncol)]
            for c, pos in enumerate(line.strip()):
                if pos == "#":
                    row_empty = False
                    col_empty[c] = False
                    galaxies.append((r, c))
            r += expand_factor if row_empty else 1
    for cidx in reversed(range(ncol)):
        if col_empty[cidx]:
            galaxies = [(r, c+expand_factor-1) if c > cidx else (r, c) for r,c in galaxies]
    return galaxies

def dist(a: Coord, b: Coord):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def short_paths(galaxies: List[Coord]):
    total = 0
    for i in range(len(galaxies)+1):
        for j in range(i+1,len(galaxies)):
            total += dist(galaxies[i], galaxies[j])
    return total

def part1():
    galaxies = get_input("2023-Day11.txt")
    return short_paths(galaxies)

def part2():
    galaxies = get_input("2023-Day11.txt", 1000000)
    return short_paths(galaxies)

# 10885634
print("part1: ", part1())

# 82000210, too low (oops, used test)
# 707505470642
print("part2: ", part2())