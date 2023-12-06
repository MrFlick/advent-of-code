import re
from math import prod
from dataclasses import dataclass

@dataclass
class Race:
    time: int
    dist: int

def dist(charge: int, race: Race):
    return (race.time - charge) * charge

def first_less_than(low, high, target, fun):
    assert(fun(low) < target)
    while high > low:
        mid = (high+low+1) // 2
        if fun(mid) >= target:
            high = mid - 1
        else:
            low = mid
    return low


def ways_to_beat(race: Race):
    tail = first_less_than(0, (race.time+1) //2, race.dist+1, lambda x: dist(x, race))
    return (race.time + 1) - (tail + 1) * 2


def get_input(path):
    with open(path) as f:
        times = (int(x) for x in re.split(r"\s+", f.readline().strip())[1:])
        dists = (int(x) for x in re.split(r"\s+", f.readline().strip())[1:])
    return list((Race(*x) for x in zip(times, dists)))


def part1():
    input = get_input("2023-Day06.txt")
    return prod(ways_to_beat(race) for race in input)


def part2():
    input = get_input("2023-Day06.txt")
    time = int("".join(str(x.time) for x in input))
    dist = int("".join(str(x.dist) for x in input))
    race = Race(time, dist)
    return ways_to_beat(race)

# 2612736
print("part1:", part1())

# 29891250
print("part2:", part2())