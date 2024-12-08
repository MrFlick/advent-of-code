from dataclasses import dataclass


@dataclass
class Equation:
    target: int
    terms: list[int]

def get_input(filename) -> list[Equation]:
    result: list[Equation] = []
    with open(filename, 'r') as file:
        for line in (x.strip() for x in file):
            target, parts = line.split(": ")
            parts = parts.split(" ")
            result.append(Equation(int(target), [int(x) for x in parts]))
    return result

input = get_input("2024-Day07.txt")

def solve(target:int, terms: list[int], allow_concat=False, current=0):
    if current == target and len(terms) == 0:
        return current
    if current > target:
        return None
    if len(terms) == 0:
        return None
    
    # not smart copying array, but easy and small
    rest = terms[1:]
    add = solve(target, rest, allow_concat, current + terms[0])
    if add is not None:
        return add
    mult = solve(target, rest, allow_concat, current * terms[0])
    if allow_concat and mult is None:
        concat = solve(target, rest, allow_concat, int(str(current) + str(terms[0])))
        return concat
    else:
        return mult

result1 = 0
result2 = 0
for i, eq in enumerate(input):
    score1 =  solve(eq.target, eq.terms)
    score2 =  solve(eq.target, eq.terms, True)
    if score1 is not None:
        result1 += score1
    if score2 is not None:
        result2 += score2

print("Part 1:", result1)
# 975671981569

print("Part 2:", result2)
# 223472064194845