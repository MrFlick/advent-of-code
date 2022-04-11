from collections import deque
from heapq import nlargest
import math

test_inputs = ["2199943210","3987894921","9856789892","8767896789","9899965678"]

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

m = [[int(y) for y in x] for x in test_inputs]

def find_lows(grid):
    R = len(grid)
    C = len(grid[0])
    lows = 0
    low_tot = 0
    for r in R:
        for c in C:
            is_low = True
            for d in dirs:
                nr, nc = r + d[0], c + d[1]
                if 0 <= nr < R and 0 <= nc < C:
                    is_low = is_low and grid[r][c] < grid[nr][nc]
            if is_low:
                lows += 1
                low_tot += grid[r][c] + 1
    return low_tot, lows


def find_basins(grid):
    R = len(grid)
    C = len(grid[0])

    visited = [[False] * C for _ in range(R)]

    def basin_size(r, c):
        q = deque()
        q.append((r, c))
        size = 0
        while q:
            r, c = q.popleft()
            if visited[r][c]: continue
            visited[r][c] = True
            size += 1
            for d in dirs:
                nr, nc = r + d[0], c + d[1]
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != 9:
                    q.append((nr, nc))
        return size
    
    basins = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] != 9 and not visited[r][c]:
                basins.append(basin_size(r, c))
    return basins

def basin_score(basins):
    return math.prod(nlargest(3,basins))


print("Basin size:", basin_score(find_basins(m)))