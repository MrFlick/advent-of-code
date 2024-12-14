from math import floor, log10


def get_input(filename: str):
    with open(filename) as f:
        return [int(x) for x in f.read().strip().split()]
    

cache: dict[tuple[int, int], int] = {}

def expand(number:int, times:int):
    if times == 0:
        return 1
    if number == 0:
        return expand(1,times-1)
    if (number, times) in cache:
        return cache[(number, times)]
    digits = floor(log10(number))+1
    if digits % 2 == 0:
        left = number // 10**(digits//2)
        right = number % 10**(digits//2)
        value = expand(left, times-1) + expand(right, times-1)
        cache[(number, times)] = value
        return value
    value = expand(number * 2024, times-1)
    cache[(number, times)] = value
    return value


def run(filename, times=25):
    input = get_input(filename)
    result = 0
    for x in input:
        result += expand(x, times)
    return result

print("Part 1:", run("2024-Day11.txt"))
# 217812

print("Part 2:", run("2024-Day11.txt", 75))
# 259112729857522