sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def get_input(filename):
    lines = []
    with open(filename, encoding="utf-8") as f:
        for nodes in (x.strip().split(" -> ") for x in f.readlines()):
            lines.append([tuple([int(z) for z in x.split(",")]) for x in nodes])
    return lines

def get_input_range(lines):
    xmin, xmax = lines[0][0][0], lines[0][0][0]
    ymin, ymax = 0, lines[0][0][1]
    for line in lines:
        for x, y in line:
            xmin = min(x, xmin)
            xmax = max(x, xmax)
            ymin = min(y, ymin)
            ymax = max(y, ymax)
    return( (xmin, xmax), (ymin, ymax))

def init_grid(lines):
    (xmin, xmax), (ymin, ymax) = get_input_range(lines)
    norm_x = lambda p: (p[0] - xmin, p[1])
    lines = [tuple([norm_x(p) for p in line]) for line in lines]
    NR = ymax - ymin + 1
    NC = xmax - xmin + 1
    grid = [["."] * NC for _ in range(NR)]
    for line in lines:
        for i in range(1, len(line)):
            dx = sign(line[i][0] - line[i-1][0])
            dy = sign(line[i][1] - line[i-1][1])
            pos = line[i-1]
            grid[pos[1]][pos[0]] = "#"
            while pos != line[i]:
                pos = (pos[0] + dx, pos[1] + dy)
                grid[pos[1]][pos[0]] = "#"
    return grid, 500-xmin

def print_grid(grid):
    for row in grid:
        print("".join(row))

dirs = ((0,1), (-1, 1), (1, 1))

def drop_sand(grid, enter):
    pos = (enter, 0)
    can_move = True
    while can_move:
        can_move = False
        for dx, dy in dirs:
            proppos = (pos[0] + dx, pos[1] + dy)
            if proppos[0] < 0 or proppos[0] >= len(grid[0]):
                #fell off side
                return True
            if proppos[1] >= len(grid):
                #fell off bottom
                return True
            if grid[proppos[1]][proppos[0]] == ".":
                # empty spot
                pos = proppos
                can_move = True
                break
    grid[pos[1]][pos[0]] = "o"
    return False
    

grid, enter = init_grid(get_input("2022-Day14.txt"))
i = 0
while True:
    result = drop_sand(grid, enter)
    if result: 
        break
    i += 1 
#print_grid(grid)
print("Part 1:", i)

#---------------------------- Part 2

def init_grid2(lines):
    grid = {}
    (xmin, xmax), (ymin, ymax) = get_input_range(lines)
    for line in lines:
        for i in range(1, len(line)):
            dx = sign(line[i][0] - line[i-1][0])
            dy = sign(line[i][1] - line[i-1][1])
            pos = line[i-1]
            grid[pos] = "#"
            while pos != line[i]:
                pos = (pos[0] + dx, pos[1] + dy)
                grid[pos] = "#"
    return grid, ymax+2

def drop_sand2(grid, bottom):
    pos = (500, 0)
    if pos in grid:
        return True
    can_move = True
    while can_move:
        can_move = False
        for dx, dy in dirs:
            proppos = (pos[0] + dx, pos[1] + dy)
            if not proppos in grid and proppos[1] < bottom:
                # empty spot
                pos = proppos
                can_move = True
                break
    grid[pos] = "o"
    return False

grid, bottom = init_grid2(get_input("2022-Day14.txt"))
i = 0
while True:
    result = drop_sand2(grid, bottom)
    if result:
        break
    i += 1 
print("Part 2:", i)