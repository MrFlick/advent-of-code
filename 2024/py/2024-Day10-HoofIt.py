from dataclasses import dataclass


@dataclass
class Grid:
    NR: int
    NC: int
    nodes: list[list[int]]


def get_grid(filename: str) -> Grid:
    with open(filename) as f:
        x =  [[int(y) for y in x.strip()] for x in f]
    return Grid(len(x), len(x[0]), x)


def spread_nines(grid: Grid, r: int, c: int, val: int, source: tuple[int, int], cache: list[list[set]]) -> None:
    for dr, dc in ((-1,0), (1, 0), (0, -1), (0, 1)):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < grid.NR and 0 <= nc < grid.NC:
            if grid.nodes[nr][nc] != val-1:
                continue
            cache[nr][nc].add(source)
            spread_nines(grid, nr, nc, grid.nodes[nr][nc], source, cache)

def spread_nines2(grid: Grid, r: int, c: int, val: int, cache: list[list[int]]) -> None:
    for dr, dc in ((-1,0), (1, 0), (0, -1), (0, 1)):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < grid.NR and 0 <= nc < grid.NC:
            if grid.nodes[nr][nc] != val-1:
                continue
            cache[nr][nc] += 1
            spread_nines2(grid, nr, nc, grid.nodes[nr][nc], cache)

from typing import Generator

def find_val(grid: Grid, val: int) -> Generator[tuple[int, int], None, None]:
    for r in range(grid.NR):
        for c in range(grid.NC):
            if grid.nodes[r][c] == val:
                yield r, c

def part1(filename):
    grid = get_grid(filename)
    cache = [[set() for _ in range(grid.NC)] for _ in range(grid.NR)]
    for r, c in find_val(grid, 9):
        spread_nines(grid, r, c, 9, (r,c), cache)
    result = 0
    for r, c in find_val(grid, 0):
        result += len(cache[r][c])
    return result

print("Part 1:", part1('2024-Day10.txt'))
# 517

def part2(filename):
    grid = get_grid(filename)
    cache = [[0 for _ in range(grid.NC)] for _ in range(grid.NR)]
    for r, c in find_val(grid, 9):
        spread_nines2(grid, r, c, 9,cache)
    result = 0
    for r, c in find_val(grid, 0):
        result += cache[r][c]
    return result

print("Part 2:", part2('2024-Day10.txt'))
# 1116