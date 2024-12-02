from dataclasses import dataclass, replace, fields
from functools import reduce
from math import prod
import re
from typing import Dict, List, Tuple

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    _part_re = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")

    def rating(self):
        return self.x + self.m + self.a + self.s

    @classmethod
    def from_str(cls, x: str):
        return Part(*(int(x) for x in cls._part_re.findall(x)[0]))

class Action:
    @classmethod
    def from_str(cls, x: str) -> "Action":
        if x == "A":
            return Accept()
        if x == "R":
            return Reject()
        if ":" in x:
            return Condition.from_str(x)
        return JumpTo(x)
    
class NoAction(Action):
    pass

@dataclass
class Condition(Action):
    var: str
    comp: str
    val: int
    if_true: Action
    if_false: Action = NoAction() # temp holder till else clause resolved

    _syntax_re = re.compile(r"([xmas])([><])(\d+):(\w+)")

    def eval(self, part: Part) -> Action:
        pval = getattr(part, self.var)
        is_true =  pval > self.val if self.comp == ">" else pval < self.val
        if is_true:
            return self.if_true
        else:
            return self.if_false

    @classmethod
    def from_str(cls, x: str):
        var, comp, val, dest = cls._syntax_re.findall(x)[0]
        return Condition(var, comp, int(val), Action.from_str(dest))

@dataclass
class JumpTo(Action):
    dest: str

class Accept(Action):
    pass

class Reject(Action):
    pass

@dataclass
class Flow:
    name: str
    action: Action = NoAction()

    _outer_re = re.compile(r"(\w+){(.*)}")

    @classmethod
    def from_str(cls, x: str):
        name, inner = cls._outer_re.findall(x)[0]
        flows = [Action.from_str(x) for x in inner.split(",")]
        # combine everything into one if/else chain
        def collapse(a: Action, b: Action):
            assert(isinstance(b, Condition))
            b.if_false = a
            return b
        action = reduce(collapse, reversed(flows))
        return Flow(name, action)
    
def get_input(path):
    flows: Dict[str, Flow] = {}
    parts: List[Part] = []
    with open(path) as f:
        should_parse_parts = False
        for line in f:
            line = line.strip()
            if not line:
                should_parse_parts = True
                continue
            if should_parse_parts:
                parts.append(Part.from_str(line))
            else:
                flow = Flow.from_str(line)
                flows[flow.name] = flow
    return flows, parts

def eval_flow(part: Part, action: Action, flows: Dict[str, Flow]):
    while True:
        if isinstance(action, Accept):
            return True
        elif isinstance(action, Reject):
            return False
        elif isinstance(action, JumpTo):
            return eval_flow(part, flows[action.dest].action, flows)
        elif isinstance(action, Condition):
            return eval_flow(part, action.eval(part), flows)
        else:
            raise Exception("Bad instance type: " + str(action.__class__))
        
@dataclass(frozen = True)
class Partition:
    x: Tuple[int, int]
    m: Tuple[int, int]
    a: Tuple[int, int]
    s: Tuple[int, int]

    def split(self, var: str, comp: str, val: int) -> List["Partition"]:
        # split a partition based on a condition
        # if never true, return []
        # if always true, return [self]
        # otherwise return 2 partitions, with first always 
        #    satisfying the condition [true_part, false_part]
        varval = getattr(self, var)
        if comp == "<":
            if val < varval[0]:
                return []
            if varval[1] < val:
                return [self]
            return [
                replace(self, **{var: (varval[0], val-1)}),
                replace(self, **{var: (val, varval[1])})
            ]
        else:
            if varval[1] <= val:
                return []
            if varval[0] > val:
                return [self]
            return [
                replace(self, **{var: (val+1, varval[1])}),
                replace(self, **{var: (varval[0], val)})
            ]
        
    def size(self):
        def rangesize(x: Tuple[int, int]):
            return x[1] - x[0] + 1 
        return prod(rangesize(getattr(self, f.name)) for f in fields(self))
    
    @classmethod
    def all_same(cls, min: int, max: int):
        return Partition(**{k.name: (min, max) for k in fields(cls)})
    
def eval_partition(part: Partition, action: Action, flows: Dict[str, Flow]):
    while True:
        if isinstance(action, Accept):
            return part.size()
        elif isinstance(action, Reject):
            return 0
        elif isinstance(action, JumpTo):
            return eval_partition(part, flows[action.dest].action, flows)
        elif isinstance(action, Condition):
            splits = part.split(action.var, action.comp, action.val)
            if len(splits) < 1:
                return 0
            elif len(splits) == 1:
                return eval_partition(part, action.if_true, flows)
            else:
                return eval_partition(splits[0], action.if_true, flows) + \
                    eval_partition(splits[1], action.if_false, flows)
        else:
            raise Exception("Bad instance type: " + action.__class__.__name__)


def part1():
    flows, parts = get_input("2023-Day19.txt")
    total = 0
    for part in parts:
        if eval_flow(part, flows["in"].action, flows):
            total += part.rating()
    return total

def part2():
    flows, _ = get_input("2023-Day19.txt")
    partition = Partition.all_same(1, 4000)
    return eval_partition(partition, flows["in"].action, flows)

# 280909
print("part 1: ", part1())

# 116138474394508
print("part 2: ", part2())