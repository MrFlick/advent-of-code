from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Pair:
    x: int
    y: int

@dataclass(frozen=True)
class Input:
    buttonA: Pair
    buttonB: Pair
    prize: Pair

    def move(self, apress, bpress):
        return Pair(self.buttonA.x * apress + self.buttonB.x * bpress, 
                    self.buttonA.y * apress + self.buttonB.y * bpress)

def get_input(filename:str):
    entry_re = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)';
    with open(filename) as f:
        input = f.read()
    # find all matches in input and extract groups
    matches = re.findall(entry_re, input, re.M)
    result = []
    for match in matches:
        result.append(Input(Pair(int(match[0]), int(match[1])), Pair(int(match[2]), int(match[3])), Pair(int(match[4]), int(match[5]))))
    return result

def solve(input: Input) -> int:
    ap = min(input.prize.x // input.buttonA.x + 1, 100)
    bp = 0
    best = -1
    while(0 <= ap <= 100):
        bp = min((input.prize.x - input.buttonA.x * ap) // input.buttonB.x, 100)
        if (input.move(ap, bp) == input.prize):
            if best < 0 or ap*3 + bp < best:
                best = ap*3 + bp
        ap -= 1
    return best 

def part1(filename: str) -> int:
    inputs = get_input(filename)
    result = 0
    for x in inputs:
        xscore = solve(x)
        if xscore > 0:
            result += xscore
    return result
    
print("Part 1", part1("2024-Day13.txt"))
# 29517