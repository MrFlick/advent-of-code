from enum import Enum
from collections import deque, defaultdict
import re

class Direction(Enum):
    NORTH=3
    EAST=0
    SOUTH=1
    WEST=2

    @classmethod
    def flip(cls, val:'Direction') -> 'Direction':
        return(Direction((val.value + 2) % 4))

    @classmethod
    def is_vertical(cls, val:'Direction') -> bool:
        return(val==Direction.NORTH or val==Direction.SOUTH)

    @classmethod
    def is_horizontal(cls, val:'Direction') -> bool:
        return(val==Direction.EAST or val==Direction.WEST)
    
    @classmethod
    def is_parallel(cls, val1:'Direction', val2:'Direction') -> bool:
        return(val1.value %2 == val2.value %2)

    @classmethod
    def will_swap(cls, val1:'Direction', val2:'Direction') -> bool:
        return val1 == val2 or \
            (val1==Direction.NORTH and val2==Direction.EAST) or \
            (val1==Direction.EAST and val2==Direction.NORTH) or \
            (val1==Direction.SOUTH and val2==Direction.WEST) or \
            (val1==Direction.WEST and val2==Direction.SOUTH)

boxrule = {
    ('A','W'): ('W','Z','Y','X'),
    ('W','A'): ('A','B','C','D'),
    ('1','4'): ('4','D','3','Z'),
    ('4','1'): ('1','X','2','B'),

    ('D','Z'): ('Z','Y','X','W'),
    ('Z','D'): ('D','A','B','C'),
    ('4','3'): ('3','C','2','Y'),
    ('3','4'): ('4','W','1','A'),

    ('C','A'): ('A','4','W','1'),
    ('A','C'): ('C','2','Y','3'),
    ('B','D'): ('D','3','Z','4'),
    ('D','B'): ('B','1','X','2'),

    ('B','X'): ('X','W','Z','Y'),
    ('X','B'): ('B','C','D','A'),
    ('1','2'): ('2','Y','3','C'),
    ('2','1'): ('1','A','4','W'),

    ('W','Y'): ('Y','3','C','2'),
    ('Y','W'): ('W','1','A','4'),
    ('Z','X'): ('X','2','B','1'),
    ('X','Z'): ('Z','4','D','3'),

    ('2','3'): ('3','Z','4','D'),
    ('3','2'): ('2','B','1','X'),
    ('Y','C'): ('C','D','A','B'),
    ('C','Y'): ('Y','X','W','Z')
}

def shift(tup, n):
    return tup[n:] + tup[0:n]

def gcd(x, y):
    while(y):
       x, y = y, x % y
    return abs(x)
 
class MapWalker():
    def __init__(self, map):
        self.map = map
        self.pos = (0, self.map[0].index(0))
        self.dir = Direction.EAST
        self.NR = len(map)
        self.NC = len(map[0])
        self.size = gcd(max(self.NR,self.NC), min(self.NR,self.NC))
        self.init_map()

    def walk(self, dist):
        nextp, nextd = self.move_direction(self.pos, self.dir)
        while self.map[nextp[0]][nextp[1]] == 0 and dist > 0:
            self.pos = nextp
            self.dir = nextd
            dist -= 1
            nextp, nextd = self.move_direction(self.pos, self.dir)

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
    
    def perform_moves(self, moves):
        for move in moves:
            if isinstance(move, int):
                self.walk(move)
            else:
                self.turn(move)

    def score(self):
        return (self.pos[0]+1)*1000 + (self.pos[1]+1)*4 + self.dir.value

class FlatMapWalker(MapWalker):
    def init_map(self):
        self.tops = [self.NR] * self.NC
        self.bots = [0] * self.NC
        self.lefts = [self.NC] * self.NR
        self.rights = [0] * self.NR
        for irow, row in enumerate(self.map):
            for ichar, char in enumerate(row):
                if char == -1:
                    continue
                self.tops[ichar] = min(self.tops[ichar], irow)
                self.bots[ichar] = max(self.bots[ichar], irow)
                self.lefts[irow] = min(self.lefts[irow], ichar)
                self.rights[irow] = max(self.rights[irow], ichar)

    def move_direction(self, pos, direction):
        if direction == Direction.NORTH:
            nr, nc = pos[0] - 1, pos[1]
            if nr < 0: nr = self.NR-1
            if self.map[nr][nc] == -1:
                nr = self.bots[nc]
            return (nr, nc), direction
        if direction == Direction.EAST:
            nr, nc = pos[0], pos[1] + 1
            if nc >= self.NC: nc = 0
            if self.map[nr][nc] == -1:
                nc = self.lefts[nr]
            return (nr, nc), direction
        if direction == Direction.SOUTH:
            nr, nc = pos[0] + 1, pos[1]
            if nr >= self.NR: nr = 0
            if self.map[nr][nc] == -1:
                nr = self.tops[nc]
            return (nr, nc), direction
        if direction == Direction.WEST:
            nr, nc = pos[0], pos[1] - 1
            if nr < 0: nr = self.NR-1
            if self.map[nr][nc] == -1:
                nc = self.rights[nr]
            return (nr, nc), direction

class BoxMapWalker(MapWalker):
    def init_map(self):
        sides =  [[self.map[i][j]>=0 for j in range(0,self.NC, self.size)] for i in range(0, self.NR, self.size)]
        mapped = {}
        q = deque()
        q.append(((0, sides[0].index(True)), ('C','A'), Direction.SOUTH))
        while q:
            face, dir, incoming = q.pop()
            if face in mapped or face[0]<0 or face[1] <0 or face[0] >= len(sides) or face[1]>=len(sides[0]) or not sides[face[0]][face[1]] :
                continue
            if incoming == Direction.NORTH:
                orient = shift(boxrule[dir], 2)
            elif incoming == Direction.WEST:
                orient = shift(boxrule[dir], 3)
            elif incoming == Direction.EAST:
                orient = shift(boxrule[dir], 1)
            else: # Direction.SOUTH 
                orient =  boxrule[dir]
            mapped[face] = orient
            q.append(((face[0]+1, face[1]), (orient[0],orient[2]), Direction.SOUTH))
            q.append(((face[0]-1, face[1]), (orient[2],orient[1]), Direction.NORTH))
            q.append(((face[0], face[1]+1), (orient[3],orient[1]), Direction.EAST))
            q.append(((face[0], face[1]-1), (orient[1],orient[3]), Direction.WEST))
        edges = defaultdict(set)
        for face, orient in mapped.items():
            edges[orient[0]].add((face, Direction.NORTH))
            edges[orient[1]].add((face, Direction.EAST))
            edges[orient[2]].add((face, Direction.SOUTH))
            edges[orient[3]].add((face, Direction.WEST))
        self.jumps = {}
        for x in [list(x) for x in edges.values()]:
            ed1 = x[0]
            ed2 = x[1]
            self.jumps[ed1] = ed2
            self.jumps[ed2] = ed1

    def move_direction(self, pos, direction):
        current_face = (pos[0] // self.size, pos[1] // self.size)
        ndist = 0
        if direction == Direction.NORTH:
            next_pos = (pos[0] - 1, pos[1])
            ndist = pos[1] - current_face[1] * self.size
        if direction == Direction.EAST:
            next_pos = (pos[0], pos[1] + 1)
            ndist = pos[0] - current_face[0] * self.size
        if direction == Direction.SOUTH:
            next_pos = (pos[0] + 1, pos[1])
            ndist = pos[1] - current_face[1] * self.size
        if direction == Direction.WEST:
            next_pos = (pos[0], pos[1] - 1)
            ndist = pos[0] - current_face[0] * self.size
        next_face = (next_pos[0] // self.size, next_pos[1] // self.size)
        if current_face == next_face:
            return next_pos, direction
        next_face, incoming_direction = self.jumps[(current_face, direction)]
        next_direcion = Direction.flip(incoming_direction)
        if Direction.will_swap(direction, incoming_direction):
            ndist = self.size - ndist - 1          
        if incoming_direction == Direction.NORTH:
            next_pos = (next_face[0] * self.size, next_face[1] * self.size + ndist)
        elif incoming_direction == Direction.SOUTH:
            next_pos = ((next_face[0] + 1) * self.size-1, next_face[1] * self.size + ndist)
        elif incoming_direction == Direction.EAST:
            next_pos = (next_face[0] * self.size + ndist, (next_face[1] + 1) * self.size - 1)
        elif incoming_direction == Direction.WEST:
            next_pos = (next_face[0] * self.size + ndist, next_face[1] * self.size)
        return next_pos, next_direcion


def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        rawmap, rawmoves = f.read().split("\n\n")
        rows = rawmap.split("\n")
        NR = len(rows)
        NC = max(len(row) for row in rows)
        map = [[-1] * NC for _ in range(NR)]
        for irow, row in enumerate(rows):
            for ichar, char in enumerate(row):
                if char == " ":
                    continue
                if char == ".":
                    map[irow][ichar] = 0
                elif char == "#":
                    map[irow][ichar] = 1
        moves = re.split('(\D+)', rawmoves)
        moves = [int(x) if x.isnumeric() else x for x in moves]
        return moves, map

def part1():
    moves, map  = get_input("2022-Day22.txt")
    walker = FlatMapWalker(map)
    walker.perform_moves(moves)
    return walker.score()

def part2():
    moves, map  = get_input("2022-Day22.txt")
    walker = BoxMapWalker(map)
    walker.perform_moves(moves)
    return walker.score()


print("Part 1: ", part1())
# Part 1:  73346
print("Part 2: ", part2())
# Part 2:  106392
