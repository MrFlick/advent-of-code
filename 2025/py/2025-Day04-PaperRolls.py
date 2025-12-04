from dataclasses import dataclass

@dataclass(frozen=False)
class Grid:
    data: list[list[str]]
    nr: int
    nc: int
    roll_count: int

def read_grid(filename: str) -> Grid:
    with open(filename, "r") as file:
        data = [list(line.strip()) for line in file.readlines()]
    return Grid(data=data, nr=len(data), nc=len(data[0]), roll_count=count_rolls(data))

def count_rolls(data: list[list[str]]) -> int:
    roll_count = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "@":
                roll_count += 1
    return roll_count

def is_removable(r: int, c: int, grid: Grid) -> bool:
    return sum(x=="@" for x in neighbors(r, c, grid)) < 4

def neighbors(r: int, c: int, grid: Grid) -> list[tuple[int, int]]:
    neighbors = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.nr and 0 <= nc < grid.nc:
                neighbors.append(grid.data[nr][nc])
    return neighbors

def sweep_grid(grid: Grid) -> Grid:
    new_data = [["." for _ in range(grid.nc)] for _ in range(grid.nr)]
    for r in range(grid.nr):
        for c in range(grid.nc):
            if grid.data[r][c] == ".":
                new_data[r][c] = "."
                continue
            if is_removable(r, c, grid):
                new_data[r][c] = "."
            else:
                new_data[r][c] = "@"
    return Grid(data=new_data, nr=grid.nr, nc=grid.nc, roll_count=count_rolls(new_data))

def part1(grid: Grid) -> int:
    result = 0
    for r in range(grid.nr):
        for c in range(grid.nc):
            if grid.data[r][c] == ".":
                continue
            if is_removable(r, c, grid):
                result += 1
    return result

def part2(grid: Grid) -> int:
    start = grid.roll_count
    new_grid = sweep_grid(grid)
    while new_grid.roll_count != grid.roll_count:
        grid = new_grid
        new_grid = sweep_grid(grid)
    return start - new_grid.roll_count

def main():
    test_grid = read_grid("2025-Day04-test.txt")
    main_grid = read_grid("2025-Day04.txt")

    print("part 1 test", part1(test_grid))
    # 13
    print("part 1 main", part1(main_grid))
    # 1389

    print("part 2 test", part2(test_grid))
    # 43
    print("part 2 main", part2(main_grid))
    # 9000
    

if __name__ == "__main__":
    main()