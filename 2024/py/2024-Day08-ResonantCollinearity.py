from collections import defaultdict
from dataclasses import dataclass
import itertools


@dataclass
class Grid:
    NR: int
    NC: int
    nodes: dict[str, list[tuple[int, int]]]

def get_input(filename):
    nodes = defaultdict(list)
    with open(filename) as f:
        for r, row in enumerate((x.strip() for x in f)):
            for c, val in enumerate(row):
                if val != '.':
                    nodes[val].append((r, c))
    return Grid(r + 1, c + 1, nodes)

def in_bounds(grid, pos):
    return 0 <= pos[0] < grid.NR and 0 <= pos[1] < grid.NC

def get_antinodes(grid: Grid, pos1, pos2):
    dr = pos2[0] - pos1[0]
    dc = pos2[1] - pos1[1]
    a = ( pos2[0] + dr, pos2[1] + dc )
    b = ( pos1[0] - dr, pos1[1] - dc )
    if in_bounds(grid, a):
        yield a
    if in_bounds(grid, b):
        yield b

def get_antinodes2(grid: Grid, pos1, pos2):
    dr = pos2[0] - pos1[0]
    dc = pos2[1] - pos1[1]
    node = (pos2[0], pos2[1])
    while in_bounds(grid, node):
        yield node
        node = (node[0] + dr, node[1] + dc)
    node = (pos1[0], pos1[1])
    while in_bounds(grid, node):
        yield node
        node = (node[0] - dr, node[1] - dc)

def draw_grid(grid, antinodes):
    for r in range(grid.NR):
        for c in range(grid.NC):
            if (r, c) in antinodes:
                print('#', end='')
            else:
                print('.', end='')
        print()


input = get_input('2024-Day08.txt')

antinodes = set()
antinodes2 = set()
for freg, positions in input.nodes.items():
    for pair in itertools.combinations(positions, 2):
        for antinode in get_antinodes(input, *pair):
                antinodes.add(antinode)
        for antinode in get_antinodes2(input, *pair):
                antinodes2.add(antinode)


print("Part 1", len(antinodes))
print("Part 2", len(antinodes2))
