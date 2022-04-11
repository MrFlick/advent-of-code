from heapq import heappop, heappush

dirs = ((1,0), (0, 1), (-1, 0), (0, -1))

with open("2021-Day15.txt") as f:
    grid = [ [int(x) for x in line.strip()] for line in f]
N = len(grid)

# Use classic A* algorightm with manhattan heuristic h()

def findminrisk(matrix, fold=1):
    q = [(0, 0, 0, 0)]
    N = len(matrix)
    M = N*fold
    best = [[-1] * M for _ in range(M)]
    grid = [[0] * M for _ in range(M)]
    for r in range(M):
        for c in range(M):
            grid[r][c]  = (matrix[r % N][c % N] + r // N + c // N - 1) % 9 + 1
    def h(r, c):
        return (M-1-r) + (M-1-c)
    while q:
        _, risk, r, c = heappop(q)
        if r==M-1 and c==M-1:
            return risk
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < M and 0 <= nc < M:
                nrisk = risk + grid[nr][nc]
                if best[nr][nc] == -1 or nrisk < best[nr][nc]:
                    heappush(q, (h(nr, nc) + nrisk, nrisk, nr, nc))
                    best[nr][nc] = nrisk

print(findminrisk(grid, fold=5))

        

