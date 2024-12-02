from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import chain, repeat
from typing import DefaultDict, Dict, Iterable, List, Set, Tuple

# Similar vibe to 10 day, keeping track of what's inside
# of the given border

class Edge(Enum):
    Bar = '|'
    OpensUp = 'U'
    OpensDown = 'D'


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def from_char(char: str):
        dirs = {"R": Direction.RIGHT,
                "D": Direction.DOWN,
                "L": Direction.LEFT,
                "U": Direction.UP}
        return dirs[char]
    
    @staticmethod
    def from_int(index: int):
        dirs = [Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT,
                Direction.UP]
        return dirs[index]
    
    def bend(self, other: "Direction") -> Edge:
        if self == Direction.DOWN or other == Direction.UP:
            return Edge.OpensUp
        elif self == Direction.UP or other == Direction.DOWN:
            return Edge.OpensDown
        else:
            raise ValueError(f"bad bend {self}, {other}")
    
@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def step(self, direction: Direction, dist=1):
        if direction == Direction.LEFT:
            return Coord(self.row, self.col-dist)
        elif direction == Direction.RIGHT:
            return Coord(self.row, self.col+dist)
        elif direction == Direction.UP:
            return Coord(self.row-dist, self.col)
        elif direction == Direction.DOWN:
            return Coord(self.row+dist, self.col)
        else:
            raise ValueError("Unknown direction")

@dataclass
class DigRecord:
    direction: Direction
    dist: int
    color: str

def get_input(path):
    result = []
    with open(path) as f:
        for line in f:
            direction, dist, color = line.strip().split(" ")
            result.append(DigRecord(Direction.from_char(direction), int(dist), color.strip("()")))
    return result

def vrange(vals: Iterable[int]):
    minv, maxv = None, None
    for x in vals:
        if minv is None or x < minv:
            minv = x
        if maxv is None or x > maxv:
            maxv = x
    assert(minv is not None and maxv is not None)
    return (minv, maxv)

def wrap_pair_iter(vals: List):
    # Take list of A, B, C, D
    # and return pairs
    # (A, B), (B, C), (C, D), (D, A)
    # * note loop back around at end
    dbl_iter = chain(chain.from_iterable(repeat(x, 2) for x in vals), [vals[0]])
    next(dbl_iter)
    return zip(dbl_iter, dbl_iter)

def trace(digs: List[DigRecord]) -> DefaultDict[int, List[Tuple[int, Edge]]]:
    # annotate corner positions
    # keep track of orientation (does it point Up or Down)
    col_events = defaultdict(list)
    pair_iter = wrap_pair_iter(digs)
    pos = Coord(0, 0)
    for a, b in pair_iter:
        assert(a.direction != b.direction)
        pos = pos.step(a.direction, a.dist)
        col_events[pos.row].append((pos.col, a.direction.bend(b.direction)))
    return col_events

def scorerow(events: List[Tuple[int, Edge]]):
    # move left to right in row, keeping track of when we are
    # "in" or "out" of the loop
    total = 0
    events.sort()
    is_in = False
    last_col = 0
    event_iter = iter(events)
    stop = False
    while not stop:
        try:
            # type will be |, U, or D
            col, type = next(event_iter)
            if type == Edge.Bar:
                total += 1
                if is_in:
                    total += max(col - last_col - 1, 0)
                is_in = not is_in
                last_col = col
            else:
                close_col, close_type = next(event_iter)
                if is_in:
                    total += max(col - last_col - 1, 0)
                if type != close_type:
                    is_in = not is_in
                total += max(close_col - col - 1, 0)
                total += 2
                last_col = close_col
        except StopIteration:
            assert(not is_in)
            stop = True
    return total

def score(events: Dict[int, List[Tuple[int, Edge]]]):
    total = 0
    downs: Set[int] = set()
    last_row = None
    rows = sorted(events.keys())
    for row, bendevents in ((k, events[k]) for k in rows):
        bendcols = set(x[0] for x in bendevents)
        downevents: List[Tuple[int, Edge]] = [(x, Edge.Bar) for x in downs]
        if last_row is not None and row != last_row + 1:
            total += scorerow(downevents) * (row-last_row-1)
        rowevents = bendevents + [(c, v) for (c, v) in downevents if c not in bendcols]
        total += scorerow(rowevents)
        for col, type in bendevents:
            if type == Edge.OpensUp:
                downs.remove(col)
            if type == Edge.OpensDown:
                downs.add(col)
        last_row = row
    return total

def recode(record: DigRecord):
    return DigRecord(Direction.from_int(int(record.color[6])), int(record.color[1:6], 16), "")

def part1():
    input = get_input("2023-Day18.txt")
    pts = score(trace(input))
    return pts

def part2():
    input = [recode(x) for x in get_input("2023-Day18.txt")]
    pts = score(trace(input))
    return pts

# 46359
print("part1: ", part1())

# 59574883048274
print("part2: ", part2())



