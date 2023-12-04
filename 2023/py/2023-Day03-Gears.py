def get_input(path):
    with open(path) as f:
        rows = f.read().splitlines()
        return [list(x) for x in rows]
    
def nei(r, c, grid):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr!=0 or dc!=0) and 0<=(r+dr)<len(grid) and 0 <= (c+dc) < len(grid[r+dr]):
                yield (r+dr, c+dc)

def check_for_symbol(positions, grid):
    for r, c in positions:
        if not grid[r][c].isdigit() and not grid[r][c] == ".":
            return True

def annotate_grid(grid):
    annotated = []
    numbers = []
    symbols = []
    for r, row in enumerate(grid):
        arow = []
        cnum = ""
        for c, col in enumerate(row + ['.']):
            if col.isdigit():
                cnum += col
                arow.append(len(numbers))
            else:
                if cnum:
                    arow.append(-1)
                    numbers.append(int(cnum))
                    cnum = ""
                else:
                    arow.append(-1)
                if col != ".":
                    symbols.append((r, c))
        annotated.append(arow)
    return annotated, numbers, symbols

def find_part_numbers(grid):
    agrid, numbers, symbols = annotate_grid(grid)
    part_indexes = set()
    for r, c in symbols:
        for nr, nc in nei(r, c, agrid):
            if agrid[nr][nc] != -1:
                part_indexes.add(agrid[nr][nc])
    return [numbers[x] for x in part_indexes]

def find_gear_ratios(grid):
    ratios = []
    agrid, numbers, symbols = annotate_grid(grid)
    for r, c in symbols:
        adj = set()
        if grid[r][c] != "*":
            continue
        adj = set(agrid[nr][nc] for nr, nc in nei(r, c, grid) if agrid[nr][nc] != -1)
        if len(adj) == 2:
            ratios.append(numbers[adj.pop()] * numbers[adj.pop()])
    return ratios

    
def part1():
    grid = get_input("2023-Day03.txt")
    part_nums = find_part_numbers(grid)
    return sum(x for x in part_nums)

def part2():
    grid = get_input("2023-Day03.txt")
    part_nums = find_gear_ratios(grid)
    return sum(x for x in part_nums)

# 521601
print("part1:", part1())

# 80694070
print("part2:", part2())