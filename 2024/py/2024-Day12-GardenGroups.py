import re
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Grid:
    NR: int
    NC: int
    nodes: list[str]

    def all_positions(self):
        for r in range(self.NR):
            for c in range(self.NC):
                yield Position(r, c)

    def val(self, pos: "Position"):
        if pos.r < 0 or pos.r >= self.NR or pos.c < 0 or pos.c >= self.NC:
            return "~"
        return self.nodes[pos.r][pos.c]

@dataclass(frozen=True)
class Position:
    r: int
    c: int

    def nei(self, grid: Grid):
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r, c = self.r + dr, self.c + dc
            yield Position(r, c)

    def tuple(self):
        return self.r, self.c

@dataclass
class Stats:
    area: int = 0
    perimiter: int = 0
    sides: int = 0

def get_input(filename: str, pattern: str):
    with open(filename) as f:
        content = f.read()
    matches = re.findall(pattern, content)
    return matches

# Example usage:
pattern = r'\d+'  # Regex pattern to match all numbers
matches = get_input("2024-Day12-test1.txt", pattern)
for match in matches:
    print(match)

def get_grid(filename:str) -> Grid:
    with open(filename) as f:
        x = [x.strip() for x in f.readlines()]
        return Grid(len(x), len(x[0]), x)
    
def walls_to_sides(walls:int):
    if walls == 15:
        return 4
    if walls in (7, 11, 13, 14):
        return 2
    if walls in (3,6,9,12):
        return 1
    return 0
    
def get_stats(filename):
    grid = get_grid(filename)
    stats = defaultdict(Stats)
    visited = set()
    gidx = 0
    for pos in grid.all_positions():
        if pos.tuple() in visited:
            continue
        inner_visited = set()
        outer_visited = set()
        queue = [pos]
        grp = grid.val(pos) + "_" + str(gidx)
        while(queue):
            walk = queue.pop()
            if walk.tuple() in inner_visited or walk in outer_visited:
                continue
            walls = 0
            for nei in walk.nei(grid):
                walls = (walls << 1)
                if grid.val(nei) != grid.val(walk):
                    walls += 1
                    stats[grp].perimiter += 1
                    outer_visited.add(nei)
                else:
                    queue.append(nei)
            stats[grp].area += 1
            visited.add(walk.tuple())
            stats[grp].sides += walls_to_sides(walls)
            inner_visited.add(walk.tuple())
        for walk in outer_visited:
            walls = 0
            
            for nei in walk.nei(grid):
                walls = (walls << 1)
                if nei.tuple() in inner_visited:
                    walls += 1
            print("Outer", walk.tuple(), walls_to_sides(walls))
        print("----")
            stats[grp].sides += walls_to_sides(walls)
        gidx += 1

    return stats

def part1(filename:str):
    stats = get_stats(filename)
    result = 0
    for group, stat in stats.items():
        result += stat.area * stat.perimiter
    return result

def part2(filename:str):
    stats = get_stats(filename)
    print(stats)
    result = 0
    for group, stat in stats.items():
        result += stat.area * stat.sides
    return result
    
#print("Part 1:", part1("2024-Day12-test1.txt"))
# 1344578

# print("Part 2:", part2("2024-Day12-test2.txt"))

assert(part1("2024-Day12-test1.txt")==140)
assert(part2("2024-Day12-test1.txt")==80)

assert(part1("2024-Day12-test2.txt")==1930)
assert(part2("2024-Day12-test2.txt")==1206)

assert(part1("2024-Day12-test3.txt")==772)
assert(part2("2024-Day12-test3.txt")==436)

assert(part2("2024-Day12-test4.txt")==236)

print("Part 2:", part2("2024-Day12-test5.txt"))
assert(part2("2024-Day12-test5.txt")==368)

