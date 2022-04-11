from heapq import nlargest
import math

dirs = ((1,0), (0, 1), (-1, 0), (0, -1))

def get_input(filename):
    grid = []
    with open(filename) as f:    
        for line in (x.strip() for x in f):
            grid.append([int(x) for x in line])
    return grid

def find_lows(grid):
    R = len(grid)
    C = len(grid[0])

    lows = []
    for r in range(R):
        for c in range(C):
            is_low = True
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    if grid[nr][nc] <= grid[r][c]:
                        is_low = False
                        break
            if is_low:
                lows.append((r, c, grid[r][c]))
    return lows

def score_lows(lows):
    risk = 0
    for _, _, v in lows:
        risk += 1 + v
    return risk

def find_basins(grid):
    R = len(grid)
    C = len(grid[0])
    visited = [[False] * C for _ in range(R)]

    def bsize(r, c):
        if not (0 <= r < R and 0 <= c < C):
            return 0
        if visited[r][c]:
            return 0
        visited[r][c] = True
        if grid[r][c] == 9:
            return 0
        size = 1
        for dr, dc in dirs:
            size += bsize(r + dr, c+dc)
        return size
    
    basins = []
    for r in range(R):
        for c in range(C):
            if not visited[r][c] and grid[r][c] != 9:
                basins.append(bsize(r, c))

    return basins

def score_basins(sizes):
    return math.prod(nlargest(3, sizes))


input = get_input("2021-Day09.txt")
print(score_lows(find_lows(input)))
print(score_basins(find_basins(input)))