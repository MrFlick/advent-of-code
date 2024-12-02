from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Deque, Dict, List, Set, Tuple


class Space(Enum):
    ROCK = "#"
    OPEN = "."
    START = "S"

Coord = Tuple[int, int]

def cadd(a: Coord, b: Coord):
    return (a[0] + b[0], a[1] + b[1])

class Grid:
    def __init__(self, grid: List[List[Space]]):
        self._grid = grid
        self.NROW = len(grid)
        self.NCOL = len(grid[0])

    def get(self, pos: Coord):
        return self._grid[pos[0]][pos[1]]
    
    def in_bounds(self, pos: Coord):
        return 0 <= pos[0] < self.NROW and \
            0 <= pos[1] < self.NCOL
    
    def next_steps(self, pos: Coord):
        for step in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            space = cadd(pos, step)
            if self.in_bounds(space) and self.get(space) != Space.ROCK:
                yield space

class GridRepeat(Grid):
    def get(self, pos: Coord):
        return self._grid[pos[0] % self.NROW][pos[1] % self.NCOL]
    
    def in_bounds(self, pos: Coord):
        return True

def get_input(path):
    grid: List[List[Space]] = []
    with open(path) as f:
        start = (0,0)
        for r, line in enumerate(f.readlines()):
            row = []
            for c, space in enumerate(list(line.strip())):
                if space == Space.ROCK.value:
                    row.append(Space.ROCK)
                else:
                    row.append(Space.OPEN)
                if space == Space.START.value:
                    start = (r, c)
            grid.append(row)
    return start, grid

def explore(start: Coord, grid: Grid, step_goal = 6):
    to_explore: Deque[Tuple[Coord, int]] = deque([(start, 0)])
    visited: Set[Coord] = set()
    total = 0
    while to_explore:
        space, steps = to_explore.popleft()
        if space in visited:
            continue
        if steps % 2 == 0:
            total += 1
            visited.add(space)
        if steps == step_goal:
            continue
        for next_space in grid.next_steps(space):
            to_explore.append((next_space, steps+1))
    return total

def part1():
    start, raw_grid = get_input("2023/py/2023-Day21.txt")
    grid = Grid(raw_grid)
    return explore(start,grid, 64)

def part2():
    start, raw_grid = get_input("2023/py/2023-Day21-test.txt")
    grid = GridRepeat(raw_grid)
    return explore(start,grid, 1000)

# 3658
print("part 1:", part1())

#print("part 2:", part2())