from itertools import chain

vents = []

with open("2021-Day05.txt") as f:
    for line in f:
        pts = line.strip().split(" -> ")
        r = []
        for p in pts:
            r.append([int(x) for x in p.split(",")])
        vents.append(r)

def grid_range(ends):
    ((maxx, maxy), (_, _)) = ends[0]
    for (x1,y1), (x2, y2) in ends:
        maxx = max(x1,x2,maxx)
        maxy = max(y1,y2,maxy)
    return (maxx+1, maxy+1)

def is_not_diag(ends):
    return ends[0][0]==ends[1][0] or ends[0][1]==ends[1][1]

def sign(x):
    if x>0: return 1
    if x<0: return -1
    return 0

def mark(grid, vent):
    (x1, y1), (x,y) = vent
    dx = sign(x1 - x)
    dy = sign(y1 - y)
    while(x != x1 or y != y1):
        grid[y][x] += 1
        x += dx
        y += dy
    grid[y][x] += 1

def overlap(grid):
    return sum(x>1 for x in chain.from_iterable(grid))

def printgrid(grid):
    for row in grid:
        print(" ".join(str(x) for x in row))

C, R = grid_range(vents)
grid = [[0] * C for _ in range(R)]

for vent in filter(is_not_diag, vents):
    mark(grid, vent)
print(overlap(grid))


grid = [[0] * C for _ in range(R)]
for vent in vents:
    mark(grid, vent)
print(overlap(grid))







