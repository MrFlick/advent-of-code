from abc import ABC, abstractmethod
from enum import Enum
from itertools import count
from typing import List, NoReturn, Tuple

ROCK = "O"
FREE = "."
WALL = "#"

Grid = List[List[str]]

def get_input(path):
    with open(path) as f:
        return [list(x.strip()) for x in f.readlines()]
    
class GridView(ABC):
    def __init__(self, grid: Grid):
        self.grid = grid
        self.NROW = len(grid)
        self.NCOL = len(grid[0])

    @abstractmethod
    def limits(self) -> Tuple[int, int]:
        pass

    def primary_range(self):
        return range(self.limits()[0])
    
    def secondary_range(self):
        return range(self.limits()[1])
    
    def in_secondary_range(self, val: int):
        return 0 <= val < self.limits()[1]

    @abstractmethod
    def tx(self, primary: int, secondary: int) -> Tuple[int, int]:
        pass
    
    def get(self, primary: int, secondary: int):
        r, c = self.tx(primary, secondary)
        return self.grid[r][c]

    def set(self, primary: int, secondary: int, val: str):
        r, c = self.tx(primary, secondary)
        self.grid[r][c] = val

class TiltSouthGridView(GridView):
    def limits(self):
        return self.NCOL, self.NROW
    
    def tx(self, primary:int, secondary: int):
        return self.NROW - secondary - 1, primary

class TiltNorthGridView(GridView):
    def limits(self):
        return self.NCOL, self.NROW
    
    def tx(self, primary:int, secondary: int):
        return secondary, primary
    
class TiltWestGridView(GridView):
    def limits(self):
        return self.NROW, self.NCOL
    
    def tx(self, primary:int, secondary: int):
        return primary, secondary
    
class TiltEastGridView(GridView):
    def limits(self):
        return self.NROW, self.NCOL
    
    def tx(self, primary:int, secondary: int):
        return primary, self.NCOL - secondary - 1
    

def slide(gv: GridView):
    for p in gv.primary_range():
        dest = 0
        for s in gv.secondary_range():
            if gv.get(p, s) == ROCK:
                if dest == s:
                    dest += 1
                else:
                    assert(gv.get(p, dest)==FREE)
                    gv.set(p, dest, ROCK)
                    gv.set(p, s, FREE)
                    while gv.in_secondary_range(dest) and gv.get(p, dest) != FREE:
                        dest += 1
            elif gv.get(p, s) == WALL:
                dest = s
                while gv.in_secondary_range(dest) and gv.get(p, dest) == WALL:
                    dest += 1
            else:
                assert(gv.get(p, s)==FREE)

def score_grid(grid: Grid):
    total = 0
    NROW = len(grid)
    for r in range(NROW):
        for c in range(len(grid[r])):
            if grid[r][c] == ROCK:
                total += NROW-r
    return total

def find_cycle(grid: Grid):
    transforms = [TiltNorthGridView, TiltWestGridView, TiltSouthGridView, TiltEastGridView]
    idx = 0
    visited = {}
    scores = []
    for cycle in count():
        for tx in transforms:
            slide(tx(grid))
        scores.append(score_grid(grid))
        key = collapse_grid(grid)
        if key in visited:
            return visited[key], cycle-1, scores
        visited[key] = cycle
        idx += 1
    return NoReturn

def collapse_grid(grid: Grid):
    return "".join("".join(r) for r in grid)

def print_grid(grid: Grid):
    for row in grid:
        print("".join(row))
    
def part1():
    input = get_input("2023-Day14.txt")
    slide(TiltNorthGridView(input))
    # print_grid(input)
    return score_grid(input)

def part2():
    input = get_input("2023-Day14.txt")
    init, first_rep, scores = find_cycle(input)
    target = 1000000000-1
    answer_idx = (target - init) % (first_rep-init+1) + init
    return scores[answer_idx]

# 109596
print("part1: ", part1())

# 96105
print("part2: ", part2())