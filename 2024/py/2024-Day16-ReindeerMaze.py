from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Generator

@dataclass(frozen=True)
class Pair:
    r: int
    c: int

    def add(self, other: "Pair") -> "Pair":
        return Pair(self.r + other.r, self.c + other.c)
    
    def dist(self, other: "Pair") -> int:
        return abs(self.r - other.r) + abs(self.c - other.c) + 1
    
    def __lt__(self, other: "Pair") -> bool:
        return (self.r, self.c) < (other.r, other.c)

@dataclass(frozen=True)
class Grid:
    walls: set[Pair]
    NR: int
    NC: int

@dataclass(frozen=True)
class Proposal:
    deer: "Deer"
    cost: int

@dataclass(frozen=True)
class Deer:
    pos: Pair
    facing: int = 0

    def moves(self) -> Generator[Proposal, None, None]:
        yield Proposal(Deer(self.pos.add(deltas[self.facing]), self.facing), 1)
        for f in ((self.facing + x) % 4 for x in (1, -1)):
            yield Proposal(Deer(self.pos.add(deltas[f]), f), 1001)

@dataclass(frozen=True)
class State:
    deer: Deer
    cost: int
    before: Pair
    est_cost: int  # Add estimated cost attribute

    def __lt__(self, other: "State") -> bool:
        return self.est_cost < other.est_cost  # Implement comparison based on estimated cost

deltas = [
    # east, south, west, north
    Pair(0, 1), Pair(1, 0), Pair(0, -1), Pair(-1, 0)
]

def get_input(filename):
    walls = set()
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, v in enumerate(line.strip()):
                if v == "S":
                    start = Pair(r, c)
                elif v == "E":
                    end = Pair(r, c)
                elif v == "#":
                    walls.add(Pair(r, c))
    return Grid(walls, r+1, c+1), Deer(start), end

def draw_grid(grid: Grid, path=None, start=None, end=None):
    rows = []
    for r in range(grid.NR):
        rows.append(["#" if Pair(r, c) in grid.walls else "." for c in range(grid.NC)])
    if path:
        pos = end
        while pos != start:
            rows[pos.r][pos.c] = "+"
            pos = path[pos]
    for r in rows:
        print("".join(r))

def part1(filename):
    grid, deer, end = get_input(filename)
    heap = []
    cache = {}
    path = {}
    start = deer.pos
    heappush(heap, (deer.pos.dist(end), State(deer, 0, deer.pos, deer.pos.dist(end))))  # Push tuple (priority, state)
    while heap:
        _, state = heappop(heap)  # Pop the tuple and get the state
        deer = state.deer
        cost = state.cost
        before = state.before
        if deer.pos == end:
            path[deer.pos] = before
            #draw_grid(grid, path, start, end)
            return cost
        if deer.pos in cache and cache[deer.pos] <= cost:
            continue
        cache[deer.pos] = cost
        path[deer.pos] = before
        for prop in deer.moves():
            if prop.deer.pos in grid.walls:
                continue
            new_cost = cost + prop.cost
            est_cost = new_cost + prop.deer.pos.dist(end)
            heappush(heap, (est_cost, State(prop.deer, new_cost, deer.pos, est_cost)))  # Push tuple (priority, state)
    return None

assert(part1("2024-Day16-test1.txt")==7036)
assert(part1("2024-Day16-test2.txt")==11048)

print("Part 1:", part1("2024-Day16.txt"))
# too high 82464