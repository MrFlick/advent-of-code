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

def widen_grid(grid: Grid) -> Grid:
    new_nodes = {}
    for k, v in grid.nodes.items():
        if v == "#":
            new_nodes[Pair(k.r, k.c*2)] = "#"
            new_nodes[Pair(k.r, k.c*2+1)] = "#"
        elif v == "O":
            new_nodes[Pair(k.r, k.c*2)] = "["
            new_nodes[Pair(k.r, k.c*2+1)] = "]"
    return Grid(new_nodes, grid.NR, grid.NC * 2)


def draw_grid(grid: Grid):
    for r in range(grid.NR):
        print("".join([grid.nodes.get(Pair(r, c), ".") for c in range(grid.NC)]))

velocity_lookup = {
    "^": Pair(-1, 0),
    "<": Pair(0, -1),
    ">": Pair(0, 1),
    "v": Pair(1, 0)
}

axis_lookup = {
    "^": "y",
    "<": "x",
    ">": "x",
    "v": "y"
}

def action(start: Pair, grid: Grid, move: str):
    velocity = velocity_lookup[move]
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

def next_front(grid, front: set[Pair], move: str) -> set[Pair] | None:
    velocity = velocity_lookup[move]
    axis = axis_lookup[move]
    next_front = set()
    for pos in front:
        step = pos.add(velocity)
        if step not in grid.nodes:
            # free space
            continue
        elif grid.nodes[step] == "#":
            # wall
            return None
        # Box        
        if axis == "x":
            if step in front:
                continue
            next_front.add(step)
            next_front.add(step.add(velocity))
        else:
            next_front.add(step)
            if grid.nodes[step] == "[":
                next_front.add(step.add(Pair(0,1)))
            elif grid.nodes[step] == "]":
                next_front.add(step.add(Pair(0,-1)))
    return next_front

def action2(start: Pair, grid: Grid, move: str):
    velocity = velocity_lookup[move]
    front = next_front(grid, {start}, move)
    fronts = []
    while True:
        if front is None:
            return start
        if len(front) == 0:
            break
        fronts.append(front)
        front = next_front(grid, front, move)
    for front in reversed(fronts):
        front = list(front) # got from set to list for stability
        vals = [grid.nodes[x] for x in front]
        for x in front:
            del grid.nodes[x]
        for p, v in zip(front, vals):
            grid.nodes[p.add(velocity)] = v
    return start.add(velocity)

def score(grid: Grid, char="O"):
    result = 0
    for k, v in grid.nodes.items():
        if v == char:
            result += 100 * k.r + k.c
    return(result)

def part1(filename):
    pos, grid, moves = get_input(filename)
    for move in moves:
        pos = action(pos, grid, move)
    return(score(grid))

def part2(filename):
    pos, grid, moves = get_input(filename)
    grid = widen_grid(grid)
    pos = Pair(pos.r, pos.c*2)
    draw_grid(grid)
    print(pos)
    for move in moves:
        pos = action2(pos, grid, move)
    return(score(grid, "["))

assert(part1("2024-Day15-test1.txt") == 2028)
assert(part1("2024-Day15-test2.txt") == 10092)

print("Part 1:", part1("2024-Day15.txt"))
# 1517819

assert(part2("2024-Day15-test2.txt") == 9021)

print("Part 2:", part2("2024-Day15.txt"))
# 1538862