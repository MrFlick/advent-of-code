from dataclasses import dataclass, field
from collections import defaultdict
from math import floor

@dataclass
class Rule:
    before: set = field(default_factory=set)
    # I never ended up using after, but I left it in anyway
    after: set = field(default_factory=set)

@dataclass
class Input:
    rules: defaultdict
    updates: list[list[str]]

def getOrdering(filename):
    ordering = defaultdict(lambda: Rule())
    reports = []
    with open(filename, "r") as file:
        it = (x.strip() for x in file)
        for line in it:
            if line == "":
                break
            left, right = line.split("|")
            ordering[right].before.add(left)
            ordering[left].after.add(right)
        for line in it:
            pages = line.split(",")
            reports.append(pages)
    return(Input(ordering, reports))

def update_sort(pages, rules):
    pages = set(pages)
    left_count = {p: len(rules[p].before & pages) for p in pages}
    return sorted(pages, key=lambda x: left_count[x])

x = getOrdering("2024-Day05.txt")
result1 = 0
result2 = 0

for input in x.updates:
    left = set()
    ok = True
    for page in input:
        if page in x.rules:
            if not left <= x.rules[page].before:
                ok = False
                break
            left.add(page)
    middle_idx = len(input)//2
    if ok:
        
        result1 += int(input[middle_idx])
    else:
        input = update_sort(input, x.rules)
        result2 += int(input[middle_idx])
    
print("Part 1:", result1)
# 4569
print("Part 2:", result2)
# 6456


