from dataclasses import dataclass
from typing import List

@dataclass
class Grid:
    rows: List[str]
    cols: List[str]

    def __nonzero__(self):
        return self.rows

def get_input(path) -> List[Grid]:
    grids = []
    with open(path) as f:
        grid = None
        for line in (x.strip() for x in f):
            if not grid:
                grid = Grid([],["" for _ in line])
            if not line:
                if grid:
                    grids.append(grid)
                    grid = None
            else:
                grid.rows.append(line)
                for c, val in enumerate(line):
                    grid.cols[c] += val
        grids.append(grid)
    return grids

def find_fold(vals: List[str]):
    for i in range(len(vals)-1):
        looks_good = True
        for j in range(min(i+1, len(vals)-i-1)):
            if vals[i-j] != vals[i+j+1]:
               looks_good = False
               break
        if looks_good:
            return i
    return -1

def find_smudge(vals: List[str]):
    mismatches = []
    result = -1
    for i in range(len(vals)-1):
        mismatch = 0
        for a, b in ((vals[i-j], vals[i+j+1]) for j in range(min(i+1, len(vals)-i-1))):
            mismatch += sum(x != y for x, y in zip(a, b))
        if mismatch == 1:
            result = i
        mismatches.append(mismatch)
    assert(sum(x==1 for x in mismatches)<=1)
    return result

def score_grid(grid: Grid):
    rf =  find_fold(grid.rows)
    cf =  find_fold(grid.cols)
    total = 0
    if cf != -1:
        total += cf + 1
    if rf != -1:
        total += 100*(rf + 1)
    return total

def score_smudge(grid: Grid):
    rf =  find_smudge(grid.rows)
    cf =  find_smudge(grid.cols)
    total = 0
    if cf != -1:
        total += cf + 1
    if rf != -1:
        total += 100*(rf + 1)
    return total


def part1():
    input = get_input("2023-Day13.txt")
    return sum(score_grid(g) for g in input)

def part2():
    input = get_input("2023-Day13.txt")
    return sum(score_smudge(g) for g in input)

# 34911
print("part1:", part1())

# 33183
print("part2:", part2())
