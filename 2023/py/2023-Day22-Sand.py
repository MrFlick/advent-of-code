from dataclasses import dataclass, field
from typing import List, Tuple

Pair = Tuple[int, int]

def range_overlap(a: Pair, b: Pair):
    return a[0] <= b[1] and a[1] >= b[0]


@dataclass(frozen=True)
class Plane():
    axis1: Pair
    axis2: Pair

    def overlaps(self, other: "Plane"):
        return range_overlap(self.axis1, other.axis1) and \
            range_overlap(self.axis2, other.axis2)

@dataclass()
class Coord3D():
    x: int
    y: int
    z: int

    def move_down(self, dist=1):
        self.z -= dist

    @staticmethod
    def from_str(x: str):
        return Coord3D(*(int(c) for c in x.strip().split(",")))

@dataclass()
class Brick():
    corner1: Coord3D
    corner2: Coord3D
    label: int
    supporting: List["Brick"] = field(default_factory = list)
    supported_by: List["Brick"] = field(default_factory = list)

    def move_down(self, dist=1):
        self.corner1.move_down(dist)
        self.corner2.move_down(dist)

    def axis_range(self, axis: str) -> Pair:
        return (
            min(getattr(self.corner1, axis), getattr(self.corner2, axis)),
            max(getattr(self.corner1, axis), getattr(self.corner2, axis))
        )

    def bottom_plane(self):
        return Plane(self.axis_range("x"), self.axis_range("y"))
    
    def add_supporting(self, brick: "Brick"):
        self.supporting.append(brick)

    def add_supported_by(self, brick: "Brick"):
        self.supported_by.append(brick)

    def bottom(self):
        return self.axis_range("z")[0]
    
    def top(self):
        return self.axis_range("z")[1]

def get_input(path):
    bricks: List[Brick] = []
    with open(path) as f:
        for i, line in enumerate(f):
            corners = [Coord3D.from_str(x) for x in line.split("~")]
            bricks.append(Brick(corners[0], corners[1], i))
    bricks.sort(key = lambda x: x.axis_range("z")[0])
    return bricks

def drop_bricks(bricks: List[Brick]):
    for i, brick in enumerate(bricks):
        candidates: List[Brick] = list()
        for j in range(0, i):
            if brick.bottom_plane().overlaps(bricks[j].bottom_plane()):
                candidates.append(bricks[j])
        top = max(b.top() for b in candidates) if candidates else 0
        drop = brick.bottom()-top-1
        brick.move_down(drop)
        for support in (b for b in candidates if b.top()==top):
            brick.add_supported_by(support)
            support.add_supporting(brick)

def part1():
    bricks = get_input("2023-Day22.txt")
    drop_bricks(bricks)
    precarious = set(brick.label for brick in bricks if len(brick.supported_by)==1)
    return sum(not any(x.label in precarious for x in brick.supporting) for brick in bricks)

# 398
print("part1: ", part1())
