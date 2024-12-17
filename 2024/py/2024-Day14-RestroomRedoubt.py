from dataclasses import dataclass
from math import prod
import re


@dataclass(frozen=True)
class Pair:
    x: int
    y: int

    def add_mod(self, add: "Pair", mod: "Pair") -> "Pair":
        return Pair((self.x + add.x) % mod.x, (self.y + add.y) % mod.y)
    
    def add(self, add: "Pair") -> "Pair":
        return Pair((self.x + add.x), (self.y + add.y))

@dataclass
class Robot:
    position: Pair
    velocity: Pair

    def step(self, dim:Pair):
        self.position = self.position.add_mod(self.velocity, dim)

def get_input(filename):
    robot_re = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)';
    with open(filename) as f:
        input = f.read()
    # find all matches in input and extract groups
    matches = re.findall(robot_re, input, re.M)
    result = []
    for match in matches:
        result.append(Robot(Pair(int(match[0]), int(match[1])), Pair(int(match[2]), int(match[3]))))
    return result

def move(robot: Robot, dim: Pair, moves:int) -> Pair:
    for _ in range(moves):
        robot.step(dim)
    return robot.position

def cmp(a, b):
    return (a > b) - (a < b)

def get_quad(pos: Pair, dim:Pair) -> tuple[int, int]:
    x =  cmp(pos.x, (dim.x)//2)
    y =  cmp(pos.y, (dim.y)//2)
    if x!=0 and y!=0:
        return (x,y)
    else:
        return (0,0)

def part1(filename):
    input = get_input(filename)
    dim = Pair(101, 103)
    quad_count = {}
    for x in input:
        end = move(x, dim, 100)
        quad = get_quad(end, dim)
        if quad != (0,0):
            quad_count[quad] = quad_count.get(quad, 0) + 1
    return prod(quad_count.values())


def draw(positions: set[Pair], dim: Pair):
    for y in range(dim.y):
        print("".join(["*" if Pair(x,y) in positions else "." for x in range(dim.x)]))

delta = [Pair(1, 0), Pair(-1, 0), Pair(0, 1), Pair(0, -1), Pair(1, 1), Pair(-1, -1), Pair(1, -1), Pair(-1, 1)]
def connected(positions: set[Pair]):
    score = 0
    for pos in positions:
        for d in delta:
            if pos.add(d) in positions:
                score += 1
    return score


def part2(filename):
    robots = get_input(filename)
    dim = Pair(101, 103)
    best_score = 0
    best_moves = 0
    for m in range(101*103):
        positions = set()
        for x in robots:
            x.step(dim)
            positions.add(x.position)
        # assume when we have a formation, a lot of points will be near each other
        score = connected(positions)/len(positions)
        if score == 0 or score > best_score:
            best_score = score
            best_moves = m + 1
            draw(positions=positions, dim=dim)
            print(best_moves, best_score)
            input()
        
        
print("Part 1:", part1("2024-Day14.txt"))
# 229069152

part2("2024-Day14.txt")
# 7383