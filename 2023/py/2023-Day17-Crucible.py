from abc import ABC
from dataclasses import dataclass
from enum import Enum
import heapq
from typing import List

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def rotate(self, change: int):
        new_val = (self.value + change) % 4
        cls = type(self)
        types = [x for x in dir(cls) if not x.startswith("__") and isinstance(cls[x], cls)]
        for t in types:
            if new_val == cls[t].value:
                return cls[t]
        raise NotImplementedError


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def step(self, direction: Direction):
        if direction == Direction.LEFT:
            return Coord(self.row, self.col-1)
        elif direction == Direction.RIGHT:
            return Coord(self.row, self.col+1)
        elif direction == Direction.UP:
            return Coord(self.row-1, self.col)
        elif direction == Direction.DOWN:
            return Coord(self.row+1, self.col)
        else:
            raise ValueError("Unknown direction")
        
    def dist_to(self, other: "Coord"):
        return abs(self.row - other.row) + abs(self.col - other.col)

class Grid:
    def __init__(self, grid: List[List[int]]):
        self._grid = grid
        self.NROW = len(grid)
        self.NCOL = len(grid[0])

    def get(self, pos: Coord):
        return self._grid[pos.row][pos.col]
    
    def is_in_bounds(self, pos: Coord):
        return 0 <= pos.row < self.NROW and \
            0 <= pos.col < self.NCOL
    
@dataclass(frozen=True)
class SearchState:
    estcost: int
    cost: int
    pos: Coord
    heading: Direction
    current_run: int

    def visit_state(self):
        return (self.pos.row, self.pos.col, self.heading, self.current_run)
    
    def __lt__(self, other):
        return self.estcost < other.estcost
    
def get_input(path):
    with open(path) as f:
        return Grid([list(int(x) for x in line.strip()) for line in f])
    
class Explorer:
    def __init__(self, grid: Grid, start: Coord, goal: Coord):
        self.grid = grid
        self.goal = goal
        self.start = start

    def init_states(self):
        raise NotImplementedError

    def next_states(self, state: SearchState):
        raise NotImplementedError
    
    
class BasicExplorer(Explorer):
    def init_states(self):
        for direction in (Direction.RIGHT, Direction.DOWN):
            next_step = self.start.step(direction)
            next_cost = self.grid.get(next_step)
            next_heur = next_cost + next_step.dist_to(self.goal)
            yield SearchState(next_heur, next_cost, next_step, direction, 0)

    def next_states(self, state: SearchState):
        if state.current_run < 2:
            next_pos = state.pos.step(state.heading)
            if self.grid.is_in_bounds(next_pos):
                next_cost = state.cost + self.grid.get(next_pos)
                next_heur = next_cost + next_pos.dist_to(self.goal)
                yield SearchState(next_heur,
                        next_cost,
                        next_pos, state.heading, state.current_run+1)
        for change in (1, -1):
            next_heading = state.heading.rotate(change)
            next_pos = state.pos.step(next_heading)
            if self.grid.is_in_bounds(next_pos):
                next_cost = state.cost + self.grid.get(next_pos)
                next_heur = next_cost + next_pos.dist_to(self.goal)
                yield SearchState(next_heur,
                        next_cost,
                        next_pos, next_heading, 0)

class UltraExplorer(Explorer):
    def init_states(self):
        for direction in (Direction.RIGHT, Direction.DOWN):
            next_step = self.start
            next_cost = 0
            for _ in range(4):
                next_step = next_step.step(direction)
                next_cost = next_cost + self.grid.get(next_step)
            next_heur = next_cost + next_step.dist_to(self.goal)
            yield SearchState(next_heur, next_cost, next_step, direction, 3)

    def next_states(self, state: SearchState):
        if state.current_run < 9:
            next_pos = state.pos.step(state.heading)
            if self.grid.is_in_bounds(next_pos):
                next_cost = state.cost + self.grid.get(next_pos)
                next_heur = next_cost + next_pos.dist_to(self.goal)
                yield SearchState(next_heur,
                        next_cost,
                        next_pos, 
                        state.heading, state.current_run+1)
        for change in (1, -1):
            next_heading = state.heading.rotate(change)
            next_pos = state.pos
            next_cost = state.cost
            is_in_bounds = True
            for _ in range(4):
                next_pos = next_pos.step(next_heading)
                if self.grid.is_in_bounds(next_pos):
                    next_cost = next_cost + self.grid.get(next_pos)
                else:
                    is_in_bounds = False
            if is_in_bounds:
                next_heur = next_cost + next_pos.dist_to(self.goal)
                yield SearchState(next_heur,
                        next_cost,
                        next_pos, next_heading, 3)


def shortest_path(explorer: Explorer):
    to_visit: List[SearchState] = []
    visited = dict()
    for state in explorer.init_states():
        heapq.heappush(to_visit, state)
    while to_visit:
        state = heapq.heappop(to_visit)
        if state.pos == explorer.goal:
            return state.cost
        if visited.get(state.visit_state(), state.cost+1) <= state.cost:
            # already found better path
            continue
        visited[state.visit_state()] = state.cost
        for next_state in explorer.next_states(state):
            heapq.heappush(to_visit, next_state)

def part1():
    input = get_input("2023-Day17.txt")
    start = Coord(0, 0)
    goal = Coord(input.NROW-1, input.NCOL-1)
    return shortest_path(BasicExplorer(input, start, goal))

def part2():
    input = get_input("2023-Day17.txt")
    start = Coord(0, 0)
    goal = Coord(input.NROW-1, input.NCOL-1)
    return shortest_path(UltraExplorer(input, start, goal))

# 722
print("part1: ", part1())

# 894
print("part2: ", part2())
