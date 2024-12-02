import sys
import re
from collections import defaultdict

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def get_data(filename):
    data = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            nums = [int(x) for x in re.findall(r'-?\d+', line)]
            data.append(((nums[0], nums[1]),(nums[2], nums[3])))
    return data

def manhat(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def cant_touch(s, b, y):
    clear_dist = manhat(s, b)
    spread = clear_dist - abs(s[1]-y)
    if spread < 0:
        return None
    return (s[0]-spread, s[0]+spread)

def is_overlapping(a, b):
    ax, ay = a
    bx, by = b
    return ax <= by and bx <= ay

def join(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def part1(data,y):
    intervals = []
    beacons = set()
    for s, b in data:
        clear_range = cant_touch(s, b, y)
        if b[1]==y:
            beacons.add((b[0], b[0]))
        if not clear_range:
            continue
        nintervals = []
        for interval in intervals:
            if is_overlapping(interval, clear_range):
                clear_range = join(clear_range, interval)
            else:
                nintervals.append(interval)
        nintervals.append(clear_range)
        intervals = nintervals
    interval_len =  sum(x[1]-x[0]+1 for x in intervals)
    overlapping_beacons = sum(any(is_overlapping(y, x) for y in intervals) for x in beacons)
    return interval_len - overlapping_beacons

# print(part1(get_data("2022-Day15-test.txt"), 10))
print("Part 1: ", part1(get_data("2022-Day15.txt"), 2000000))
# Part 1:  5166077

# Part 2 -----------------

# If there's going to be only one spot, it's going to have to be on an "edge"
# of a visible region. Since those are diagonal lines, they greatly reduce 
# search space. The idea is that the missing beacon is going to be at the
# intersction of at least two of these edge lines. So find the edges, then
# find the intersections. Then check only those points for visibility

def can_see(s, b, point):
    d = manhat(s, b)
    return manhat(s, point) <= d

def get_outer_vertexes(s, b):
    d = manhat(s, b)
    return (
        (s[0], s[1] - d - 1), # top
        (s[0] + d + 1, s[1]), # right
        (s[0], s[1] + d + 1), # bottom
        (s[0] - d - 1, s[1]), # left
    )

def get_lines(s, b):
    v = get_outer_vertexes(s, b)
    yield((v[0], v[1]))
    yield((v[1], v[2]))
    yield((v[2], v[3]))
    yield((v[3], v[0]))

def get_line_param(p1, p2):
    s = (p2[1]-p1[1]) // (p2[0]-p1[0])
    return (-s, 1, s*p1[0]-p1[1])

def get_intersection(line1, line2):
    det = (line1[0] * line2[1] - line2[0] * line1[1])
    if det == 0:
        return None
    point = (
        (line1[1] * line2[2] - line2[1] * line1[2])//det,
        (line2[0] * line1[2] - line1[0] * line2[2])//det
    )
    return point

def is_point_between(p1, p2, p):
    return sign(p1[0]-p[0]) != sign(p2[0]-p[0]) and sign(p1[1]-p[1]) != sign(p2[1]-p[1])

def find_possible_intersction(v1, v2):
    point = get_intersection(get_line_param(v1[0], v1[1]), get_line_param(v2[0], v2[1]))
    if not point:
        return None
    if is_point_between(v1[0], v1[1], point) and is_point_between(v2[0], v2[1], point):
        return point
    return None

# print(find_possible_intersction(((1,1), (3,3)), ((1,10), (10,1))))
# print(find_possible_intersction(((1,1), (6,6)), ((1,10), (10,1))))

def part2(data, cap):
    candidates = defaultdict(int)
    for i in range(0, len(data)-1):
        for j in range(i+1, len(data)):
            s1,b1 = data[i]
            s2,b2 = data[j]

            for v1 in get_lines(s1, b1):
                for v2 in get_lines(s2, b2):
                    point = find_possible_intersction(v1, v2)
                    if point and 0 <= point[0] <= cap and 0 <= point[1] <= cap:
                        candidates[point] +=1

    for point in [k for k, v in candidates.items() if v >=4 ]:
        solution = True
        for s, b in data:
            if can_see(s, b, point):
                solution = False
                break
        if solution:
            return point[0]*4000000 + point[1]

# print(part2(get_data("2022-Day15-test.txt"), 20))
print("Part 2: ", part2(get_data("2022-Day15.txt"), 4000000))
# Part 2:  13071206703981
