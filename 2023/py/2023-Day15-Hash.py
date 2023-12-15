from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterable, List
import re

@dataclass
class Command:
    pass

@dataclass
class PutCommand(Command):
    label: str
    box: int
    focal: int

@dataclass
class TakeCommand(Command):
    label: str
    box: int


def get_input(path):
    with open(path) as f:
        return f.readline().strip().split(",")

def hash(x: str):
    total = 0
    for c in x:
        total += ord(c)
        total *= 17
        total %= 256
    return total

def hash_cmds(cmds: List[str]):
    return sum((hash(cmd) for cmd in cmds))

def parse_cmd(cmd: str) -> Command:
    parts = re.split(r"([-=])", cmd)
    if len(parts)<2:
        raise Exception(f"Invalid command {cmd}")
    if parts[1] == "=":
        assert(len(parts)==3)
        return PutCommand(parts[0], hash(parts[0]), int(parts[2]))
    elif parts[1] == "-":
        return TakeCommand(parts[0], hash(parts[0]))
    else:
        raise Exception(f"Invalid command {cmd}")
    
def execute_commands(cmds: Iterable[Command]):
    # a regular dict should be ordered as well
    # but just making it clear we rely on this property
    boxes = [OrderedDict() for _ in range(256)]
    for cmd in cmds:
        if isinstance(cmd, PutCommand):
            boxes[cmd.box][cmd.label] = cmd.focal
        elif isinstance(cmd, TakeCommand):
            if cmd.label in boxes[cmd.box]:
                boxes[cmd.box].pop(cmd.label)
        else:
            raise Exception("Invalid command")
    return boxes

def score_boxes(boxes: List[OrderedDict]):
    total = 0
    for i, box in enumerate(boxes):
        for slot, (_, focal) in enumerate(box.items()):
            box = (i + 1) * (slot + 1) * focal
            total += box
    return total

def part1():
    input = get_input("2023-Day15.txt")
    return hash_cmds(input)

def part2():
    input = get_input("2023-Day15.txt")
    return score_boxes(execute_commands(parse_cmd(x) for x in input))

assert(hash("HASH") == 52)

# 522547
print("part1: ", part1())

# 229271
print("part2: ", part2())