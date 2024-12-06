from dataclasses import dataclass, replace
from enum import Enum


class Direction(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    def __init__(self, dr, dc):
        self.dr = dr
        self.dc = dc
    
    def turn90right(self) -> "Direction":
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }[self]
    
    def next(self, pos: tuple[int, int]) -> tuple[int, int]:
        r, c = pos
        return (r+self.dr, c+self.dc)

    UP = -1, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    LEFT = 0, -1

@dataclass
class Guard:
    pos: tuple[int, int] = (0,0)
    direction: Direction = Direction.UP

@dataclass
class Grid:
    NR: int
    NC: int
    obstacles: set[tuple[int, int]]

def get_input(filename):
    obstacles = set()
    with open(filename, 'r') as file:
        for r, row in enumerate(file):
            for c, cell in enumerate(row):
                if cell == "#":
                    obstacles.add((r, c))
                if cell == "^":
                    guard = Guard(pos=(r, c))
    return(Grid(r+1, c+1, obstacles), guard)

def in_bounds(grid, pos):
    r, c = pos
    return 0 <= r < grid.NR and 0 <= c < grid.NC

grid, guard_start = get_input("2024-Day06.txt")
guard = replace(guard_start)
path = set()
path.add(guard.pos)
next_pos = guard.direction.next(guard.pos)
while in_bounds(grid, next_pos):
    if next_pos in grid.obstacles:
        guard.direction = guard.direction.turn90right()
    else:
        path.add(next_pos)
        guard.pos = next_pos
    next_pos = guard.direction.next(guard.pos)

def does_loop(grid, guard):
    states = set()
    states.add((guard.pos, guard.direction))
    while in_bounds(grid, guard.pos):
        next_pos = guard.direction.next(guard.pos)
        if (next_pos, guard.direction) in states:
            return True
        if next_pos in grid.obstacles:
            guard.direction = guard.direction.turn90right()
        else:
            guard.pos = next_pos
        states.add((guard.pos, guard.direction))
    return False

print("Part 1:", len(path))
# 4515

can_loop = 0
i = 0
for p in path:
    if p == guard_start.pos:
        continue
    guard = replace(guard_start)
    grid.obstacles.add(p)
    if does_loop(grid, guard):
        can_loop += 1
    grid.obstacles.remove(p)
    i += 1

print("Part 2:", can_loop)
# 1309
# sloooow solution but it works

