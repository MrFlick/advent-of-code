import math
from heapq import heappop, heappush

def get_input(filename):
    storms = []
    with open(filename, encoding="utf-8") as f:
        rows = [x.strip() for x in f.readlines()]
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                pos = (r-1, c-1)
                if cell == ">":
                    storms.append([pos, (0, 1)])
                elif cell == "<":
                    storms.append([pos, (0, -1)])
                elif cell == "v":
                    storms.append([pos, (1, 0)])
                elif cell == "^":
                    storms.append([pos, (-1, 0)])
    NR = len(rows)-2
    NC = len(rows[0])-2
    return storms, NR, NC, math.lcm(NR, NC)

def get_states(storms, NR, NC, period):
    states = []
    for i in range(period):
        m = [[0] * NC for _ in range(NR)]
        for i in range(len(storms)):
            m[storms[i][0][0]][storms[i][0][1]] = 1
            storms[i][0] = (
                (storms[i][0][0] + storms[i][1][0]) % NR,
                (storms[i][0][1] + storms[i][1][1]) % NC)
        states.append(m)
    return states, NR, NC

def print_state(state):
    for row in state:
        print("".join("." if x==0 else "X" for x in row))

def nei(r, c, NR, NC):
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1),(0,0)):
        if 0 <= r + dr < NR and 0 <= c + dc < NC:
            yield (r + dr, c + dc)


def search(states, time, start, end):
    period = len(states)
    NR = len(states[0])
    NC = len(states[0][0])
    q = []
    visited = dict()
    dist = lambda x,y: abs(x[0]-y[0]) + abs(x[1]-y[1])
    heappush(q, (time + dist(start, end), time, start[0], start[1]))
    while q:
        _, time, r, c = heappop(q)
        if r == end[0] and c == end[1]:
            return time
        for nr, nc in nei(r, c, NR, NC):
            if states[(time+1) % period][nr][nc] == 0:
                if (time+1, nr, nc) not in visited:
                    visited[(time+1, nr, nc)] = (time, r, c)
                    heappush(q, (time+1 + dist((nr, nc), end), time+1, nr, nc))
    return None

def part1():
    states, NR, NC = get_states(*get_input("2022-Day24.txt"))
    time = 1
    result = None
    while result is None:
        while states[time][0][0] != 0:
            time += 1
        result = search(states, time, (0,0), (NR-1, NC-1))
        time += 1
    return result + 1

def part2():
    states, NR, NC = get_states(*get_input("2022-Day24.txt"))
    period = len(states)
    time = 1
    result = None
    while result is None:
        while states[time][0][0] != 0:
            time += 1
        result = search(states, time, (0,0), (NR-1, NC-1))
        time += 1
    time = result + 2
    result = None
    while result is None:
        while states[time % period][NR-1][NC-1] != 0:
            time += 1
        result = search(states, time, (NR-1,NC-1), (0, 0))
        time += 1
    time = result + 2
    result = None
    while result is None:
        while states[time % period][0][0] != 0:
            time += 1
        result = search(states, time, (0, 0), (NR-1,NC-1))
        time += 1
    return result + 1

print("Part 1:", part1())
# 185 - too low (v not V)
# Part 1: 262
print("Part 2:", part2())
# Part 2: 785