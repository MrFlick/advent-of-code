from functools import reduce
import re
import math
from itertools import cycle
from dataclasses import dataclass, field
from typing import List, NoReturn

@dataclass
class Cycle:
    offset: int
    length: int
    goal_positions: List[int] = field(default_factory=lambda: [0])

    def goals(self):
        base = self.offset
        while True:
            for goal in self.goal_positions:
                yield base + goal
            base += self.length

def get_input(path):
    nodes_re = re.compile(r'[1-9A-Z]+')
    paths = {}
    with open(path) as f:
        directions = f.readline().strip()
        f.readline()
        for line in f:
            nodes = nodes_re.findall(line)
            paths[nodes[0]] = (nodes[1], nodes[2])
    return directions, paths

def annotated_cycle(vals):
    seq = 0
    while True:
        for i, val in enumerate(vals):
            yield val, i , seq

def next_node(current_node, direction, paths):
    if direction== "L":
        return paths[current_node][0]
    elif direction == "R":
        return paths[current_node][1]
    else:
        raise Exception(f"Bad direction {direction}")


def find_cycle(start_node, directions, paths) -> Cycle:
    visited = {}
    path = []
    dirs = annotated_cycle(directions)
    current_node = start_node
    step = 0
    for d, i, _ in dirs:
        state = (current_node, i)
        if state in visited:
            offset = visited[state]
            cycle_length = step - offset
            goals = [i for i,x in enumerate(path[offset:]) if x.endswith("Z")]
            return Cycle(offset, cycle_length, goals)
        path.append(current_node)
        visited[state] = step
        current_node = next_node(current_node, d, paths)
        step += 1
    return NoReturn

def part1():
    directions, paths = get_input("2023-Day08.txt")
    current_node='AAA'
    steps = 0
    for d in cycle(directions):
        steps += 1
        current_node = next_node(current_node, d, paths)
        if current_node == 'ZZZ':
            return steps
        
def part2():
    directions, paths = get_input("2023-Day08.txt")
    current_nodes = [x for x in paths.keys() if x.endswith("A")]
    cycles = [find_cycle(n, directions, paths) for n in current_nodes]
    for c in cycles:
        assert(c.goal_positions[0] + c.offset == c.length)
    # once you have the cycle/repitiion length, for each ghost to 
    # find a goal, we just need to find the
    # lowest common multiple for when they will all be on goal
    return reduce(math.lcm, (x.length for x in cycles))

# 19199
print("part 1: ", part1())

# 13,663,968,099,527
print("part 2: ", part2())
        

