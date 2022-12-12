from heapq import heappush, heappop

def get_grid():
    def translate(x:str):
        if x.islower():
            return(ord(x)-96)
    with open("2022-Day12.txt", encoding="utf-8") as f:
        rows = [list(x.strip()) for x in f.readlines()]

    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if col.islower():
                rows[i][j] = ord(col)-96                
            elif col == "S":
                rows[i][j] = 1
                start = (i, j)
            elif col == "E":
                rows[i][j] = 26
                end = (i, j)
    return rows, start, end

dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
def nei(pos, NR, NC):
    for dx, dy in dirs:
        nextp = (pos[0] + dx, pos[1] + dy)
        if 0 <= nextp[0] < NR and 0 <= nextp[1] < NC:
            yield nextp
        

def solve1():
    q = []
    grid, start, end = get_grid()
    NR = len(grid)
    NC = len(grid[0])
    heappush(q, (0, start))
    visited = set()
    visited.add(start)
    while q:
        dist, pos = heappop(q)
        if pos == end:
            return dist
        for nextp in nei(pos, NR, NC):
            if nextp not in visited:
                if grid[nextp[0]][nextp[1]] <= grid[pos[0]][pos[1]] + 1:
                    visited.add(nextp)
                    heappush(q, (dist + 1, nextp))

print("Part 1:", solve1())
# 437

def solve2():
    q = []
    grid, _, start = get_grid()
    NR = len(grid)
    NC = len(grid[0])
    heappush(q, (0, start))
    visited = set()
    visited.add(start)
    while q:
        dist, pos = heappop(q)
        if grid[pos[0]][pos[1]] == 1:
            return dist
        for nextp in nei(pos, NR, NC):
            if nextp not in visited:
                if grid[nextp[0]][nextp[1]] >= grid[pos[0]][pos[1]] - 1:
                    visited.add(nextp)
                    heappush(q, (dist + 1, nextp))

print("Part 2:", solve2())