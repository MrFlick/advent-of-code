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
    est_cost: int
    path: set[Pair]

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

def draw_grid(grid: Grid, seats = None):
    rows = []
    for r in range(grid.NR):
        rows.append(["#" if Pair(r, c) in grid.walls else "." for c in range(grid.NC)])
    if seats:
        for pos in seats:
            rows[pos.r][pos.c] = "O"
    for r in rows:
        print("".join(r))

def solve(filename):
    grid, deer, end = get_input(filename)
    heap = []
    cache = {}
    best = None
    good_seats = set()
    heappush(heap, (deer.pos.dist(end), State(deer, 0, deer.pos.dist(end), {deer.pos})))
    while heap:
        est_cost, state = heappop(heap)  # Pop the tuple and get the state
        deer = state.deer
        cost = state.cost
        path = state.path
        if best is not None and est_cost > best:
            break
        if deer.pos == end:
            if best is None or cost == best:
                best = cost
                good_seats.update(path)
            continue
        # if (deer.pos, deer.facing) in cache and cache[(deer.pos, deer.facing)] <= cost:
        #     continue
        # cache[(deer.pos, deer.facing)] = cost
        for prop in deer.moves():
            if prop.deer.pos in grid.walls:
                continue
            new_cost = cost + prop.cost
            est_cost = new_cost + prop.deer.pos.dist(end)-1
            heappush(heap, (est_cost, State(prop.deer, new_cost, est_cost, path | {prop.deer.pos})))
    return grid, best, good_seats

def part1(filename):
    _, cost, _ = solve(filename)
    return cost

def part2(filename):
    grid, _, seats = solve(filename)
    return len(seats)

#assert(part1("2024-Day16-test1.txt")==7036)
#assert(part1("2024-Day16-test2.txt")==11048)

assert(part2("2024-Day16-test1.txt")==45)
assert(part2("2024-Day16-test2.txt")==64)

# print("Part 1:", part1("2024-Day16.txt"))
# 82460

print("Part 2:", part2("2024-Day16.txt"))
# 82460