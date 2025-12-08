from math import prod
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Input:
    columns: list[str]
    ops: list[str]

def get_input(file_path: str) -> Input:
    with open(file_path, "r") as file:
        lines = file.readlines()
    ops = re.split(r"\s+", lines[-1].strip())
    starts = [i for i, c in enumerate(lines[-1]) if c != " " and c != "\n"]
    ends = [i -1 for i in starts[1:]] + [len(lines[-1])]

    columns = [[] for _ in range(len(ops))]
    for line in lines[:-1]:
        vals = [line[start:end] for start, end in zip(starts, ends)]
        for i, val in enumerate(vals):
            columns[i].append(val)
    return Input(columns=columns, ops=ops)

def part1(input: Input) -> int:
    result = 0
    for i, op in enumerate(input.ops):
        if op == "+":
            result += sum(int(col) for col in input.columns[i])
        elif op == "*":
            result += prod(int(col) for col in input.columns[i])
    return result

def part2(input: Input) -> int:
    result = 0 
    for i, op in enumerate(input.ops):
        cols = [0] * len(input.columns[i][0])
        for val in input.columns[i]:
            for i, d in enumerate(val):
                if d != " ":
                    cols[i] = cols[i] * 10 + int(d)
        if op == "+":
            result += sum(cols)
        elif op == "*":
            result += prod(cols)
    return result


def main():
    input_main = get_input("2025-Day06.txt")
    input_test = get_input("2025-Day06-test.txt")

    print("part 1 test", part1(input_test))
    # 4277556
    print("part 1 main", part1(input_main))
    # 5335495999141

    print("part 2 test", part2(input_test))
    # 3263827
    print("part 2 main", part2(input_main))
    # 10142723156431

if __name__ == "__main__":
    main()