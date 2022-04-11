from collections import defaultdict
from dataclasses import dataclass


sampleinput1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
sampleinput2  = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
sampleinput3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

#sample = [x.split("-") for x in sampleinput3.split()]
sample = [x.strip().split("-") for x in open("2021-Day12.txt").readlines()]

paths = defaultdict(set)
for start, end in sample:
    paths[start].add(end)
    paths[end].add(start)


def find_paths(start, sofar = None, path=None):
    if sofar is None:
        sofar = set()
    if path is None:
        path = []
    path.append(start)
    good = 0
    for nextd in paths[start] - sofar:
        if nextd == "end":
            path.append("end")
            #print(path)
            path.pop()
            good += 1
        else:
            is_small = start == start.lower()
            if is_small:
                sofar.add(start)
            good += find_paths(nextd, sofar, path)
            if is_small:
                sofar.remove(start)
    path.pop()
    return good

print(find_paths("start"))

def find_paths2(start, sofar = None, doubled = None, path = None):
    if sofar is None:
        sofar = set()
    if path is None:
        path = []
    path.append(start)
    good = 0
    should_remove = False
    is_small = start == start.lower()
    if start in sofar:
        if doubled is None and start != 'start':
            doubled = start
        else:
            path.pop()
            return 0
    elif is_small:
        sofar.add(start)
        should_remove = True
    
    for nextd in paths[start]:
        if nextd == "end":
            path.append("end")
            #print(",".join(path))
            path.pop()
            good += 1
        else:
            good += find_paths2(nextd, sofar, doubled, path)

    if should_remove:
        sofar.remove(start)
    path.pop()
    return good

print(find_paths2("start"))


    
