from operator import le


def read_grid(file_path: str) -> list[list[int]]:
    with open(file_path, "r") as file:
        return [[int(char) for char in line.strip()] for line in file.readlines()]

def best_row_pair(row: list[int]) -> int:
    a = 0
    for i in range(len(row)-1):
        if (row[i] > row[a]):
            a = i
    b = a + 1
    for i in range(b, len(row)):
        if (row[i] > row[b]):
            b = i
    return row[a] * 10 + row[b]

def best_number(numbers: list[int], size: int = 12) -> int:

    cache = {} # tuple (start index, size) -> best number
               # probably should have been an array for faster lookup since it's
               # densely populated
    N = len(numbers)
    # fill in base cases
    for i in range(size):
        cache[(N-1-i, i+1)] = numbers[N-1-i] * 10**i + cache.get((N-i, i), 0)
    # work backwards from small sides to large ones
    # from the end of the list.
    # We take the better of
    #  - the largest s digit number from the numbers to the left
    #  - the current number in front of the best s-1 sized number from the left
    # order of traversal is imporant for the cache to be valid
    for s in range(1, size+1):
        for i in range(N-s-1, -1, -1):
            best = max(numbers[i] * 10**(s-1) + cache.get((i+1, s-1), 0), cache.get((i+1, s), 0))
            cache[(i, s)] = best
    return cache.get((0, size), 0)

def part1(data: list[list[int]]) -> int:
    total = 0
    for row in data:
        total += best_row_pair(row)
        # can also use solution from part 2
        # total += best_number(row, 2) 
    return total

def part2(data: list[list[int]]) -> int:
    total = 0
    for row in data:
        total += best_number(row, 12)
    return total

def main():
    test_data = read_grid("2025-Day03-test.txt")
    main_data = read_grid("2025-Day03.txt")

    print("part 1 test", part1(test_data))
    # 357
    print("part 1 main", part1(main_data))
    # 17524

    print("part 2 test", part2(test_data))
    # 3121910778619
    print("part 2 main", part2(main_data))
    # 173848577117276


if __name__ == "__main__":
    main()