from typing import List

ROCK = "O"

def get_input(path):
    with open(path) as f:
        return [list(x.strip()) for x in f.readlines()]
    
def slide_north(grid: List[List[str]]):
    for c in range(len(grid[0])):
        dest = 0
        for r in range(len(grid)):
            if grid[r][c] == ROCK:
                if dest == r:
                    dest += 1
                else:
                    assert(grid[dest][c]==".")
                    grid[dest][c] = ROCK
                    grid[r][c] = "."
                    while dest < len(grid) and grid[dest][c] != ".":
                        dest += 1
            elif grid[r][c] == "#":
                dest = r
                while dest < len(grid) and grid[dest][c] == "#":
                    dest += 1
            else:
                assert(grid[r][c]==".")

def score_grid(grid: List[List[str]]):
    total = 0
    NROW = len(grid)
    for r in range(NROW):
        for c in range(len(grid[r])):
            if grid[r][c] == ROCK:
                total += NROW-r
    return total

def print_grid(grid: List[List[str]]):
    for row in grid:
        print("".join(row))
    
def part1():
    input = get_input("2023/py/2023-Day14.txt")
    slide_north(input)
    print_grid(input)
    return score_grid(input)

# 109596
print("part1: ", part1())