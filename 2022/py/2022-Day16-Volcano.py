import re
from dataclasses import dataclass
from heapq import heappop, heappush

@dataclass
class Valve:
    name: str
    flow_rate: int
    connects_to: list[str]

@dataclass
class Entity:
    pos: str
    time: int

def get_data(filename) -> dict[str, Valve]:
    valves = {}
    pattern = re.compile(r"Valve (.*?) has flow rate=(.*?); tunnels? leads? to valves? (.*)")
    with open(filename, encoding="utf-8") as f:
        for line in f:
            matches = pattern.match(line)
            valves[matches.group(1)] = Valve(matches.group(1), int(matches.group(2)), matches.group(3).split(", "))
    return valves

class Distances:
    def __init__(self, valves: dict[str, Valve]):
        self.valves = valves
        self.cache = dict()

    def lookup(self, a, b):
        if (a,b) in self.cache:
            return self.cache[(a, b)]
        q = [(0, a)]
        visited = set([a])
        while q:
            dist, pos = heappop(q)
            if pos == b:
                self.cache[(a,b)] = dist
                return dist
            for x in self.valves[pos].connects_to:
                if x in visited:
                    continue
                visited.add(x)
                heappush(q, (dist+1, x))
        return None

def explore():
    valves = get_data("2022-Day16.txt")
    hot_valves = set([k for k, v in valves.items() if v.flow_rate>0])
    dist = Distances(valves)

    def inner(pos, time=30, pressure=0, path=[]):
        if time < 1:
            return 0, path
        path = path + [pos]
        best = pressure
        bpath = path
        for v in [valves[v] for v in hot_valves]:
            d = dist.lookup(pos, v.name)
            if time < d+1:
                continue
            hot_valves.remove(v.name)
            result, rpath = inner(v.name, time = time - d - 1, pressure = pressure + v.flow_rate * (time - d - 1), path = path)
            hot_valves.add(v.name)
            if result > best:
                best = result
                bpath = rpath
        return best, bpath

    return inner("AA")[0]

#print("Part 1:", explore())
# 1720 too low (error in distance calculation)
# 2019 too high (tried different start)
# 1845
