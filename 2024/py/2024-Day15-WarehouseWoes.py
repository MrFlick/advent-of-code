from dataclasses import dataclass

@dataclass(frozen=True)
class Pair:
    r: int
    c: int

    def add(self, other: "Pair") -> "Pair":
        return Pair(self.r + other.r, self.c + other.c)

@dataclass(frozen=True)
class Grid:
    nodes: dict[Pair, str]
    NR: int
    NC: int

def get_input(filename):
    grid = {}
    moves = []
    r = 0
    with open(filename) as f:
        lineiter = iter(f)
        while True:
            line = next(lineiter).strip()
            if line == "":
                break
            for c, v in enumerate(line):
                if v == "@":
                    start = Pair(r, c)
                elif v in ("#", "O"):
                    grid[Pair(r, c)] = v
            r += 1
        for line in lineiter:
            moves.extend(x for x in line.strip())
    return start, Grid(grid, r, c+1), moves


def draw_grid(grid: Grid):
    for r in range(grid.NR):
        print("".join([grid.nodes.get(Pair(r, c), ".") for c in range(grid.NC)]))

delta = {
    "^": Pair(-1, 0),
    "<": Pair(0, -1),
    ">": Pair(0, 1),
    "v": Pair(1, 0)
}

def action(start: Pair, grid: Grid, move: str):
    velocity = delta[move]
    step = start.add(velocity)
    if step not in grid.nodes:
        # free space
        return step
    elif grid.nodes[step] == "#":
        # wall
        return start
    # fish
    path = [step]
    while True:
        step = step.add(velocity)
        if step not in grid.nodes:
            for fish in reversed(path):
                grid.nodes[fish.add(velocity)] = grid.nodes[fish]
                del grid.nodes[fish]
            return start.add(velocity)
        if grid.nodes[step] == "#":
            # wall
            return start
        path.append(step)

def score(grid: Grid):
    result = 0
    for k, v in grid.nodes.items():
        if v == "O":
            result += 100 * k.r + k.c
    return(result)

def part1(filename):
    pos, grid, moves = get_input(filename)
    for move in moves:
        pos = action(pos, grid, move)
    return(score(grid))

assert(part1("2024-Day15-test1.txt") == 2028)
assert(part1("2024-Day15-test2.txt") == 10092)

print("Part 1:", part1("2024-Day15.txt"))
# 1517819