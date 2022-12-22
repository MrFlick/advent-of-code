from enum import Enum
import re

class Direction(Enum):
    NORTH=3
    EAST=0
    SOUTH=1
    WEST=2


class MapWalker():
    def __init__(self, map, tops, bots, lefts, rights):
        self.map = map
        self.tops = tops
        self.bots = bots
        self.lefts = lefts
        self.rights = rights
        self.pos = (0, self.tops.index(0))
        self.dir = Direction.EAST
        self.NR = len(map)
        self.NC = len(map[0])

    def move_direction(self, pos, direction):
        if direction == Direction.NORTH:
            nr, nc = pos[0] - 1, pos[1]
            if nr < 0: nr = self.NR-1
            if self.map[nr][nc] == -1:
                nr = self.bots[nc]
            return (nr, nc)
        if direction == Direction.EAST:
            nr, nc = pos[0], pos[1] + 1
            if nc >= self.NC: nc = 0
            if self.map[nr][nc] == -1:
                nc = self.lefts[nr]
            return (nr, nc)
        if direction == Direction.SOUTH:
            nr, nc = pos[0] + 1, pos[1]
            if nr >= self.NR: nr = 0
            if self.map[nr][nc] == -1:
                nr = self.tops[nc]
            return (nr, nc)
        if direction == Direction.WEST:
            nr, nc = pos[0], pos[1] - 1
            if nr < 0: nr = self.NR-1
            if self.map[nr][nc] == -1:
                nc = self.rights[nr]
            return (nr, nc)

    def walk(self, dist):
        nextp = self.move_direction(self.pos, self.dir)
        while self.map[nextp[0]][nextp[1]] == 0 and dist > 0:
            self.pos = nextp
            dist -= 1
            nextp = self.move_direction(self.pos, self.dir)

    def turn(self, turn):
        if turn == 'L':
            self.dir = Direction((self.dir.value - 1) % 4)
        else:
            self.dir = Direction((self.dir.value + 1) % 4)
    
    def print(self):
        for ir, row in enumerate(self.map):
            for ic, col in enumerate(row):
                if self.pos[0]==ir and self.pos[1]==ic:
                    print("&", end="")
                elif self.map[ir][ic] == 0:
                    print(".", end="")
                elif self.map[ir][ic] == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            print("")
    
    def score(self):
        return (self.pos[0]+1)*1000 + (self.pos[1]+1)*4 + self.dir.value

def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        rawmap, rawmoves = f.read().split("\n\n")
        rows = rawmap.split("\n")
        NR = len(rows)
        NC = max(len(row) for row in rows)
        map = [[-1] * NC for _ in range(NR)]
        tops = [NR] * NC
        bots = [0] * NC
        lefts = [NC] * NR
        rights = [0] * NR
        for irow, row in enumerate(rows):
            for ichar, char in enumerate(row):
                if char == " ":
                    continue
                if char == ".":
                    map[irow][ichar] = 0
                elif char == "#":
                    map[irow][ichar] = 1
                tops[ichar] = min(tops[ichar], irow)
                bots[ichar] = max(bots[ichar], irow)
                lefts[irow] = min(lefts[irow], ichar)
                rights[irow] = max(rights[irow], ichar)
        moves = re.split('(\D+)', rawmoves)
        moves = [int(x) if x.isnumeric() else x for x in moves]
        return moves, MapWalker(map, tops, bots, lefts, rights)

def part1():
    moves, walker  = get_input("2022-Day22.txt")
    print(moves)
    for move in moves:
        if isinstance(move, int):
            walker.walk(move)
        else:
            walker.turn(move)
    walker.print()
    print(walker.score())

part1()
