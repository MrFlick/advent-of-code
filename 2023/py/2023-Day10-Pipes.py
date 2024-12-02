from dataclasses import dataclass
from typing import List, NoReturn, Set, Tuple

Coord = Tuple[int, int]

@dataclass
class Direction:
    up: bool
    down: bool
    left: bool
    right: bool

    def invert(self):
        return Direction(self.down, self.up, self.right, self.left)
    
    def op_xor(self, other: "Direction"):
        return Direction(self.up ^ other.up, self.down ^ other.down,
                           self.left ^ other.left, self.right ^ other.right)
    
    def headings(self):
        if self.up:
            yield Direction(True, False, False, False)
        if self.down:
            yield Direction(False ,True, False, False)
        if self.left:
            yield Direction(False, False, True, False)
        if self.right:
            yield Direction(False, False, False, True)

class Board:
    def __init__(self, grid):
        self.grid = grid
        self.NROW = len(self.grid)
        self.NCOL = len(self.grid[0])

    def get_value(self, pos: Coord):
        return self.grid[pos[0]][pos[1]]

    def get_connection(self, pos: Coord) -> Direction:
        return tiles[self.grid[pos[0]][pos[1]]]
    
    def set(self, pos: Coord, value: str):
        self.grid[pos[0]][pos[1]] = value


class Walker:
    def __init__(self, start: Coord, board: Board, heading: Direction):
        self.pos = start
        self.board = board
        self.heading = heading
        self.steps = 0

    def step(self, pos, direction: Direction):
        return (pos[0] + direction.up * -1 + direction.down * 1,
                pos[1] + direction.left * -1 + direction.right * 1)

    def next(self):
        next_pos = self.step(self.pos, self.heading)
        self.heading = self.heading.invert().op_xor(self.board.get_connection(next_pos))
        self.steps += 1
        self.pos = next_pos
        return next_pos

def get_input(path) -> Tuple[Coord, Board]:
    start = (0,0)
    grid = []
    with open(path) as f:
        for row, line in enumerate(f.readlines()):
            if "S" in line:
                start = (row, line.index("S"))
            grid.append(list(line.strip()))
    board = Board(grid)
    board.set(start, infer_start(start, board))
    return start, board

tiles = {
    "|": Direction(True, True, False, False),
    "-": Direction(False, False, True, True),
    "L": Direction(True, False, False, True),
    "J": Direction(True, False, True, False),
    "7": Direction(False, True, True, False),
    "F": Direction(False, True, False, True),
    ".": Direction(False, False, False, False)
}

def infer_start(pos, board: Board) -> str:
    up = board.get_connection((pos[0]-1, pos[1])).down
    down = board.get_connection((pos[0]+1, pos[1])).up
    left = board.get_connection((pos[0], pos[1]-1)).right
    right = board.get_connection((pos[0], pos[1]+1)).left
    target = Direction(up, down, left, right)
    for tile, candidate in tiles.items():
        if target == candidate:
            return tile
    return NoReturn

def wipe_line(start, board: Board, path: Set[Coord]):
    is_in_loop = False # are we "in" the loop or "out" of the loop
    is_on_pipe = False
    start_orientation = None
    end_orientation = None
    inside_count = 0
    for pos in ((start[0], c) for c in range(board.NCOL)):
        if pos in path:
            if board.get_value(pos) == "|":
                is_in_loop = not is_in_loop
            elif board.get_value(pos) == "-": # must be on a segment
                assert(is_on_pipe)
                pass
            elif is_on_pipe: # must be a bend (end of a segment)
                # the "inness" or "outness" of points
                # only changes if the ends of the pipe
                # segment point in opposite up/down directions
                con = board.get_connection(pos)
                end_orientation = Direction(con.up, con.down, False, False)
                if start_orientation != end_orientation:
                    is_in_loop = not is_in_loop
                is_on_pipe = False
            else:  # must be a bend (start of a segment)
                is_on_pipe = True
                con = board.get_connection(pos)
                start_orientation = Direction(con.up, con.down, False, False)
        else:
            inside_count += is_in_loop
    return inside_count

def wipe_grid(board: Board, path: Set[Coord]):
    total = 0
    for x in ((r, 0) for r in range(board.NROW)):
        total += wipe_line(x, board, path)
    return total


def part1():
    start, board = get_input("2023-Day10.txt")
    board.set(start, infer_start(start, board))
    # send two walkers in opposite directions, whereever
    # they meet must be the furthest point
    walkers = [Walker(start, board, h) for h in board.get_connection(start).headings()]
    while True:
        for w in walkers:
            w.next()
        if walkers[0].pos == walkers[1].pos:
            break
    return walkers[0].steps

def part2():
    start, board = get_input("2023-Day10.txt")
    path = set()
    walker = Walker(start, board, list(board.get_connection(start).headings())[0])
    path.add(walker.pos)
    walker.next()
    while walker.pos != start:
        path.add(walker.pos)
        walker.next()
    return wipe_grid(board, path)

# 6897
print("part 1:", part1())

# 367
print("part 2:", part2())