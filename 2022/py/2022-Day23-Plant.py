from collections import defaultdict

delta = {
    "n": (-1, 0),
    "s": (1, 0),
    "e": (0, 1),
    "w": (0, -1)
}

def shift(tup, n):
    return tup[n:] + tup[0:n]

def get_input(filename):
    elves = set()
    with open(filename, encoding="utf-8") as f:
        for row, line in enumerate(x.strip() for x in f.readlines()):
            for col, val in enumerate(line):
                if val == "#":
                    elves.add((row, col))
    return elves

def get_elf_range(elves):
    for e in elves:
        ymin, xmin = e
        ymax, xmax = e
        break
    for e in elves:
        xmin = min(xmin, e[1])
        xmax = max(xmax, e[1])
        ymin = min(ymin, e[0])
        ymax = max(ymax, e[0])
    return (xmin, ymin), (xmax, ymax)

def print_elves(elves):
    (xmin, ymin), (xmax, ymax) = get_elf_range(elves)
    for row in range(ymin, ymax+1):
        print("".join("#" if x else "." for x in ((row, col) in elves for col in range(xmin, xmax+1))))

def nei(pos, elves):
    return [(row+pos[0], col+pos[1]) in elves for row in range(-1,2) for col in range(-1,2) if row!=0 or col !=0]

def consider(direction, availability):
    if direction == 'n':
        return not(availability[0] or availability[1] or availability[2])
    if direction == 's':
        return not(availability[5] or availability[6] or availability[7])
    if direction == 'w':
        return not(availability[0] or availability[3] or availability[5])
    if direction == 'e':
        return not(availability[2] or availability[4] or availability[7])

def propose(directions, elves):
    proposed = defaultdict(set)
    for elf in elves:
        avail = nei(elf, elves)
        if not any(avail):
            proposed[elf].add(elf)
            continue
        moved = False
        for direction in directions:
            if consider(direction, avail):
                moved = True
                d = delta[direction]
                proposed[(elf[0] + d[0], elf[1] + d[1])].add(elf)
                break
        if not moved:
            proposed[elf].add(elf)
    return proposed

def resolve(proposed):
    resolved = set()
    moved = 0
    for newp, oldp in proposed.items():
        if len(oldp) == 1:
            if not newp in oldp:
                moved += 1
            resolved.add(newp)
        else:
            resolved.update(oldp)
    return resolved, moved

def run():
    elves = get_input("2022-Day23.txt")
    directions = ('n','s','w','e')
    round = 0
    while True:
        round += 1
        proposed = propose(directions, elves)
        elves, moved = resolve(proposed)
        directions = shift(directions, 1)
        if round == 10:
            (xmin, ymin), (xmax, ymax) = get_elf_range(elves)
            score = (xmax-xmin+1) * (ymax-ymin+1) - len(elves)
            print("Part 1:", score)
        if moved < 1:
            print("Part 2:", round)
            break

run()
# Part 1: 4068
# Part 2: 968