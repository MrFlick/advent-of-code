from dataclasses import dataclass, asdict
import re
from collections import deque

@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    def add(self, ele):
        return Resources(self.ore + ele.ore, self.clay + ele.clay, 
            self.obsidian + ele.obsidian, self.geode + ele.geode)
    def sub(self, ele):
        return Resources(self.ore - ele.ore, self.clay - ele.clay, 
            self.obsidian - ele.obsidian, self.geode - ele.geode)

@dataclass(frozen=True)
class Robot:
    type: str
    resources: Resources

@dataclass(frozen=True)
class Blueprint:
    id: int
    robots: list[Robot]

def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        def tokens(data):
            for line in data.split("\n"):
                for match in re.findall(r'(Blueprint (\d+)|(\w+) robot|and|(\d+) (\w+))', line):
                    if match[1] != '':
                        yield(('blueprint', int(match[1])))
                    elif match[2] != '':
                        yield(('robot', match[2]))
                    elif match[3] != '':
                        yield(('resource', int(match[3]), match[4]))
                    elif match[0]=="and":
                        continue
                yield(('end',))

        q = deque(tokens(f.read()))
        blueprints = []
        while q:
            bp = q.popleft()
            bprobots = []
            while q and q[0][0] == "robot":
                robot = q.popleft()
                rdata = {}
                while q and q[0][0] == "resource":
                    resource = q.popleft()
                    rdata[resource[2]] = resource[1]
                robot = Robot(robot[1], Resources(**rdata))
                bprobots.append(robot)
            bp = Blueprint(bp[1], list(reversed(bprobots)))
            assert(q.popleft()[0] == "end")
            blueprints.append(bp)

        return blueprints


def best_build(bp:Blueprint):
    start = {"ore": 1}

    def will_make(robot: Robot, robots: dict[str, int]):
        return all(k in robots for k, v in asdict(robot.resources).items() if v>0)

    def can_make(robot: Robot, inventory: Resources):
        return inventory.ore >= robot.resources.ore  and \
            inventory.clay >= robot.resources.clay  and \
            inventory.obsidian >= robot.resources.obsidian

    skipped = 0
    def can_beat(inventory: Resources, robots, time, best_score):
        nonlocal bp
        nonlocal skipped
        if inventory.geode >= best_score:
            return True
        remain = 25-time
        if (best_score - inventory.geode) > remain*(remain+1)//2:
            skipped += 1
            return False
        return True

    def inner(robots: dict[str, int], inventory: Resources, next_make=-1, time = 24, so_far_best=0, path=tuple()) -> Resources:

        if time <= 0:
            print(so_far_best, skipped, path)
            return inventory

        if not can_beat(inventory, robots, time, so_far_best):
            return Resources()
        
        #spend
        if next_make != -1:
            build = {r.type: 0 for r in bp.robots}
            if can_make(bp.robots[next_make], inventory=inventory):
                inventory = inventory.sub(bp.robots[next_make].resources)
                build[bp.robots[next_make].type] += 1
                path = path + (25-time, bp.robots[next_make].type)
                next_make = -1
                #next_make = q.popleft() ## TESTING
            inventory = inventory.add( Resources(**robots))
            robots = {k: v + robots.get(k, 0) for k,v in build.items()}
            return inner(robots, inventory, next_make, time-1, max(so_far_best, inventory.geode), path)
        else:
            best = Resources(**asdict(inventory))
            for i, robot in enumerate(bp.robots):
                build = {r.type: 0 for r in bp.robots}
                npath = path
                ninventory = Resources(**asdict(inventory))
                if can_make(robot, inventory):
                    ninventory = inventory.sub(robot.resources)
                    build[robot.type] = 1
                    npath = path + (25-time, robot.type)
                    next_make = -1
                elif will_make(robot, robots):
                    next_make = i
                else:
                    continue
                #collect
                ninventory = ninventory.add( Resources(**robots))
                #harvest
                nrobots = {k: v + robots.get(k, 0) for k,v in build.items()}
                ninv = inner(nrobots, ninventory, next_make, time-1, max(so_far_best, ninventory.geode), npath)
                if ninv.geode > best.geode:
                    best = ninv
            return best

    return inner(start, Resources()).geode

bps = get_input("2022-Day19-test.txt")
print(best_build(bps[0]))
#bests = [best_build(bp) for bp in bps]
#print(bests)
#print("Part 1:", max(bests))