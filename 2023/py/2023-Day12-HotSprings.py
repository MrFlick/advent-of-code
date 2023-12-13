from dataclasses import dataclass
from typing import List
from concurrent.futures import ProcessPoolExecutor

@dataclass
class Puzzle:
    input: str
    runs: List[int]

@dataclass
class PuzzleState:
    input_index: int
    current_run_index: int
    current_run_length: int

    def add_run(self):
        return PuzzleState(self.input_index+1, self.current_run_index, self.current_run_length+1)
    
    def add_full_run(self, runs: List[int]):
        return PuzzleState(self.input_index+runs[self.current_run_index], self.current_run_index + 1, 0)
    
    def close_run(self):
        return PuzzleState(self.input_index+1, self.current_run_index+1, 0)
    
    def start_run(self):
        return PuzzleState(self.input_index+1, self.current_run_index, 1)
    
    def add_break(self):
        return PuzzleState(self.input_index+1, self.current_run_index, 0)
    
    def min_length_req(self, runs: List[int]):
        if self.current_run_index >= len(runs):
            return 0
        remain = runs[self.current_run_index:]
        return  sum(remain) + len(remain) - 1 - self.current_run_length

def get_input(path):
    result = []
    with open(path) as f:
        for line in f:
            input, raw_runs = line.strip().split(" ")
            runs = [int(x) for x in raw_runs.split(",")]
            result.append(Puzzle(input, runs))
    return result

def setchar(string: str, pos: int, val:str) -> str:
    assert(pos < len(string))
    return string[0:pos] + val + string[pos+1:]

def unfold(p: Puzzle)->Puzzle:
    return Puzzle("?".join([p.input] * 5), p.runs * 5)

def solve(p: Puzzle) -> int:
    init = PuzzleState(0, 0, 0)
    last_run_index = p.input.rfind("#")
    def check_state(ps: PuzzleState, input, runs):
        prev = input[ps.input_index-1] if ps.input_index>0 else "."
        if ps.input_index == len(input):
            return int(ps.current_run_index == len(runs))
        if ps.current_run_index >= len(runs) and ps.input_index <= last_run_index:
            # round all runs, but still more to come
            return 0
        if ps.min_length_req(runs) > len(input) - ps.input_index:
            # not long enough
            return 0
        current = input[ps.input_index]
        if current == "?":
            return check_state(ps, setchar(input, ps.input_index, "."), runs) + \
                check_state(ps, setchar(input, ps.input_index, "#"), runs)
        elif current == "#":
            if ps.current_run_index>=len(runs):
                return 0
            can_add = True
            for i in range(runs[ps.current_run_index]):
                if i>=len(input) or input[ps.input_index+i]==".":
                    can_add = False
                    break
            if can_add:
                nextps = ps.add_full_run(runs)
                setchar(input, nextps.input_index-1, "#")
                if nextps.input_index < len(input):
                    if input[nextps.input_index] == "#":
                        return 0
                    nextps = nextps.add_break()
                    setchar(input, nextps.input_index-1, ".")
            else:
                return 0
            return check_state(nextps, input, runs)
        else: # current == ".":
            nextps = ps.add_break()
            return check_state(nextps, input, runs)
    
    return check_state(init, p.input, p.runs)


def part1():
    input = get_input("2023/py/2023-Day12.txt")
    total = 0
    for p in input:
        x = solve(p)
        print(x, p)
        total += x
    return total

def part2():
    input = [unfold(x) for x in get_input("2023/py/2023-Day12.txt")]
    total = 0
    with ProcessPoolExecutor() as executor:
        results = executor.map(solve, input)
        for result in results:
            print(result)
            total += result
    #for i, p in reversed(list(enumerate(input))):
    #    print(p)
    #    total += solve(p)
    #    print(i, "/", len(input))
    return total

if __name__ == '__main__':
    # 11511, too high (didn't check length of last run)
    # 7110
    # print("part1: ", part1())

    print("part2: ", part2())
