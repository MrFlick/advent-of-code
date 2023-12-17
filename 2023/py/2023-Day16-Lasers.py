from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Set

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def is_vertical(self):
        return self.name in ('UP','DOWN')
    
    def is_horizontal(self):
        return self.name in ('LEFT','RIGHT')

class Space(Enum):
    Empty = "."
    MirrorIncline = "/"
    MirrorDecline = "\\"
    SplitterVertical = "|"
    SlitterHorizontal = "-"

    @classmethod
    def from_str(cls, label):
        types = [x for x in dir(cls) if not x.startswith("__") and isinstance(cls[x], cls)]
        for t in types:
            if label == cls[t].value:
                return cls[t]
        raise NotImplementedError

@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def step(self, direction: Direction):
        if direction == Direction.LEFT:
            return Coord(self.row, self.col-1)
        elif direction == Direction.RIGHT:
            return Coord(self.row, self.col+1)
        elif direction == Direction.UP:
            return Coord(self.row-1, self.col)
        elif direction == Direction.DOWN:
            return Coord(self.row+1, self.col)
        else:
            raise ValueError("Unknown direction")

class Grid:
    def __init__(self, grid):
        self._grid = grid
        self.NROW = len(grid)
        self.NCOL = len(grid[0])

    def get(self, pos: Coord) -> Space:
        return self._grid[pos.row][pos.col]
    
    def in_bounds(self, pos: Coord):
        return 0 <= pos.row < self.NROW and \
            0 <= pos.col < self.NCOL
    
    def edges(self, heading: Direction):
        if heading == Direction.RIGHT:
            return (Coord(r, 0) for r in range(self.NROW))
        elif heading == Direction.LEFT:
            return (Coord(r, self.NCOL-1) for r in range(self.NROW))
        elif heading == Direction.UP:
            return (Coord(self.NROW-1, c) for c in range(self.NCOL))
        elif heading == Direction.DOWN:
            return (Coord(0, c) for c in range(self.NCOL))

def get_input(path):
    grid = []
    with open(path) as f:
        for line in f:
            grid.append([Space.from_str(x) for x in list(line.strip())])
    return Grid(grid)

def shoot_laser(grid: Grid, start_pos = Coord(0,0), start_heading = Direction.RIGHT) -> int:
    visited = set()
    to_visit = deque()
    to_visit.append((start_heading, start_pos))
    while to_visit:
        heading, pos = to_visit.popleft()
        if (heading, pos) in visited:
            continue
        if not grid.in_bounds(pos):
            continue
        space = grid.get(pos)
        if space == Space.Empty or \
                space == Space.SlitterHorizontal and heading.is_horizontal() or \
                space == Space.SplitterVertical and heading.is_vertical():
            to_visit.append((heading, pos.step(heading)))
        elif space == Space.SlitterHorizontal and heading.is_vertical():
            to_visit.append((Direction.LEFT, pos.step(Direction.LEFT)))
            to_visit.append((Direction.RIGHT, pos.step(Direction.RIGHT)))
        elif space == Space.SplitterVertical and heading.is_horizontal():
            to_visit.append((Direction.UP, pos.step(Direction.UP)))
            to_visit.append((Direction.DOWN, pos.step(Direction.DOWN)))
        elif space == Space.MirrorIncline and heading == Direction.RIGHT or \
                space == Space.MirrorDecline and heading == Direction.LEFT:
            to_visit.append((Direction.UP, pos.step(Direction.UP)))
        elif space == Space.MirrorIncline and heading == Direction.LEFT or \
                space == Space.MirrorDecline and heading == Direction.RIGHT:
            to_visit.append((Direction.DOWN, pos.step(Direction.DOWN)))
        elif space == Space.MirrorIncline and heading == Direction.DOWN or \
                space == Space.MirrorDecline and heading == Direction.UP:
            to_visit.append((Direction.LEFT, pos.step(Direction.LEFT)))
        elif space == Space.MirrorIncline and heading == Direction.UP or \
                space == Space.MirrorDecline and heading == Direction.DOWN:
            to_visit.append((Direction.RIGHT, pos.step(Direction.RIGHT)))
        else:
            raise Exception((space, pos, heading))
        visited.add((heading, pos))
    positions = set(x[1] for x in visited)
    return len(positions)


def part1():
    input = get_input("2023-Day16.txt")
    return shoot_laser(input)

def part2():
    input = get_input("2023-Day16.txt")
    best = 0
    for heading in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
        for start in input.edges(heading):
            best = max(best, shoot_laser(input, start, heading))
    return best

# 7870
print("part1: ", part1())

# 8143
print("part2: ", part2())

