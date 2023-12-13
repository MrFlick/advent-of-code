from dataclasses import dataclass
from typing import List
from functools import cache

@dataclass
class Puzzle:
    input: str
    runs: List[int]

def get_input(path):
    result = []
    with open(path) as f:
        for line in f:
            input, raw_runs = line.strip().split(" ")
            runs = [int(x) for x in raw_runs.split(",")]
            result.append(Puzzle(input, runs))
    return result


def unfold(p: Puzzle)->Puzzle:
    return Puzzle("?".join([p.input] * 5), p.runs * 5)

def solve(p: Puzzle) -> int:

    @cache # the secret to not taking forever
    def check_state(next_add: str, input_index: int, next_run_index:int):
        if input_index == len(p.input):
            if next_run_index==len(p.runs):
                return 1
            else:
                return 0
        if next_add == "#":
            if next_run_index >= len(p.runs):
                return 0
            if p.runs[next_run_index] + input_index > len(p.input):
                return 0
            for i in range(p.runs[next_run_index]):
                if p.input[input_index + i] == ".":
                    return 0
            return check_state(".", input_index + p.runs[next_run_index], next_run_index+1)
        else: #next_add == "."
            if next_run_index == len(p.runs):
                for size in range(len(p.input)-input_index):
                    if p.input[input_index + size] == "#":
                        return 0
                return 1
            total = 0
            possible_break_sizes = range(len(p.input)-(input_index + len(p.runs[next_run_index:]) -1 + sum(p.runs[next_run_index:])))
            for size in possible_break_sizes:
                if p.input[input_index + size] == "#":
                    break
                total += check_state("#", input_index + size + 1, next_run_index)
            return total
    
    return check_state(".", 0, 0) + check_state("#", 0, 0)


def part1():
    input = get_input("2023-Day12.txt")
    return sum(solve(p) for p in input)

def part2():
    input = [unfold(x) for x in get_input("2023-Day12.txt")]
    return sum(solve(p) for p in input)

# 11511, too high (didn't check length of last run)
# 7110
print("part1: ", part1())

# 1566786613613
print("part2: ", part2())
