from collections import defaultdict, deque, Counter
import re
from itertools import product
from dataclasses import dataclass, field
import operator

@dataclass
class Scanner:
    points: list = field(default_factory=list)
    orientation: int = -1
    flip: int = -1
    pdist: dict = None
    location = None
    id: int = None

axistxs = [
    lambda x: x,
    lambda x: (x[0], x[2], x[1]),
    lambda x: (x[1], x[0], x[2]),
    lambda x: (x[1], x[2], x[0]),
    lambda x: (x[2], x[0], x[1]),
    lambda x: (x[2], x[1], x[0])
]

fliptxs = [
    lambda x: x,
    lambda x: (-x[0], x[1], x[2]),
    lambda x: (x[0], -x[1], x[2]),
    lambda x: (x[0], x[1], -x[2]),
    lambda x: (-x[0], -x[1], x[2]),
    lambda x: (x[0], -x[1], -x[2]),
    lambda x: (-x[0], x[1], -x[2]),
    lambda x: (-x[0], -x[1], -x[2])
]

scanners = defaultdict(Scanner)

with open("2021-Day19.txt") as f:
    sname = ""
    for line in (x.strip() for x in f):
        if line.startswith("---"):
            m = re.search("--- scanner (\d+) ---", line)
            sname = m.group(1)
        elif line == "":
            sname = ""
        else:
            scanners[sname].points.append(tuple([int(x) for x in line.split(",")]))
            scanners[sname].id = int(sname)

def pairwise(coords):
    result = defaultdict(list)
    for i in range(len(coords)-1):
        for j in range(i+1, len(coords)):
            dist = [abs(a-b) for a, b in zip(coords[i], coords[j])]
            key = tuple(sorted(dist))
            result[key].append({"d": tuple(dist), "i": i, "j":j})
    return result

def pairwisetr(coords, tri):
    tr = axistxs[tri]
    result = defaultdict(list)
    for i in range(len(coords)-1):
        for j in range(i+1, len(coords)):
            dist = [abs(a-b) for a, b in zip(coords[i], coords[j])]
            key = tuple(tr(dist))
            result[key].append({"i": i, "j":j})
    return result


def oriento0(base, tx):
    if base == 0: return tx
    p = (1,2,3)
    for ti, tr in enumerate(axistxs):
        if tr(axistxs[tx](axistxs[base](p))) == p:
            return ti

def flipto0(base, tx):
    if base == 0: return tx
    p = (1,2,3)
    for ti, tr in enumerate(fliptxs):
        if tr(fliptxs[tx](fliptxs[base](p))) == p:
            return ti


def orient(scanners, refscanner='0'):
    partners = defaultdict(set)
    identified = set(refscanner)
    ref = scanners[refscanner]
    ref.orientation = 0
    ref.flip = 0
    ref.location = (0, 0, 0)
    todo = deque([x for x in scanners.keys() if x not in identified])
    while todo:
        refs = todo.popleft()
        ref = scanners[refs]
        match_found = False
        for s, other in [kv for kv in scanners.items() if kv[0] in identified]:
            cand = list(set(ref.pdist.keys()) & set(other.pdist.keys()))
            matches = [0] * 6
            for c in cand:
                for a, b in product(ref.pdist[c], other.pdist[c]):
                    for ti, tf in enumerate(axistxs):
                        if a["d"] == tf(b["d"]):
                            matches[ti] += 1
            best = max(matches)
            if best >= 12:
                txi = matches.index(max(matches))
                ref.orientation = oriento0(txi, other.orientation)
                identified.add(refs)
                partners[refs].add(s)
                partners[s].add(refs)
                match_found = True
        if not match_found:
            todo.append(refs)
    return partners

def match(s1, s2):
    mapping = defaultdict(Counter)
    overlap = list(set(s1.pdist.keys()) & set(s2.pdist.keys()))
    for d in overlap:
        if len(s1.pdist[d]) > 1: continue
        if len(s2.pdist[d]) > 1: continue
        s1i, s1j = s1.pdist[d][0]["i"], s1.pdist[d][0]["j"]
        s2i, s2j = s2.pdist[d][0]["i"], s2.pdist[d][0]["j"]
        mapping[s1i][s2i] += 1
        mapping[s1i][s2j] += 1
        mapping[s1j][s2i] += 1
        mapping[s1j][s2j] += 1
    if len(mapping)<6:
        return False
    
    flips = Counter()
    for k, v in mapping.items():
        if sum(x != 1 for x in v.values()) == 1:
            s1id = k
            s2id = v.most_common(1)[0][0]
            p1 = fliptxs[s1.flip](axistxs[s1.orientation](s1.points[s1id]))
            p1 = tuple(map(operator.add, p1, s1.location))
            p2 = axistxs[s2.orientation](s2.points[s2id])
            for i in range(len(fliptxs)):
                pf = fliptxs[i](p2)
                dx = (p1[0]-pf[0], p1[1]-pf[1], p1[2]-pf[2], i)
                flips[dx] += 1
    best = flips.most_common(1)[0]
    if best[1] == len(mapping):
        dx, dy, dz, fi = best[0]
        s2.location = (dx, dy, dz)
        if s2.flip == -1:
            s2.flip = fi
        return True
    return False

def normal_points(s):
    for b in s.points:
        rpos = fliptxs[s.flip](axistxs[s.orientation](b))
        pos = tuple(map(operator.add, rpos, s.location))
        yield pos

def calibrate(overlap, refscanner='0'):
    identified = set(refscanner)
    todo = deque(set(overlap.keys()) - identified)
    while todo:
        sname = todo.popleft()
        me = scanners[sname]
        matched = False
        for refs in overlap[sname]:
            if refs not in identified: continue
            ref = scanners[refs]
            if match(ref, me):
                matched = True
                identified.add(sname)
        if not matched:
            todo.append(sname)


for k, v in scanners.items():
    v.pdist = pairwise(v.points)
scanner_overlap = orient(scanners)

for k, v in scanners.items():
    v.pdist = pairwisetr(v.points, v.orientation)
    
calibrate(scanner_overlap)
beacons = Counter()
for s in scanners.values():
    for b in normal_points(s):
        beacons[b] += 1
print(len(beacons))



