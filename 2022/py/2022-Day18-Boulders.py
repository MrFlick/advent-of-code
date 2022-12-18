from collections import deque

def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        return [tuple(map(lambda x: int(x), z.strip().split(","))) for z in f.readlines()]

def nei(pos):
    x, y, z  = pos
    yield((x-1, y, z))
    yield((x+1, y, z))
    yield((x, y-1, z))
    yield((x, y+1, z))
    yield((x, y, z-1))
    yield((x, y, z+1))



def part1():
    input = set(get_input("2022-Day18.txt"))
    
    # a BFS search to count faces of connected cubes
    def count_faces(pos, cubes):
        q = deque([pos])
        count = 0
        visited = set([pos])
        while q:
            pos = q.popleft()
            for n in nei(pos):
                if n in cubes:
                    if not n in visited:
                        q.append(n)
                        visited.add(n)
                else:
                    count += 1
        return count, visited

    remain = input.copy()
    total = 0

    # loop throuh call connected groups and then
    # remove them from list till it's empty
    while remain:
        start = remain.pop()
        count, visited = count_faces(start, input)
        remain -= visited
        total += count
    return total

print("Part 1:", part1())
# Part 1: 4348

def part2():
    input = set(get_input("2022-Day18.txt"))

    # find observed range and expand by 1 to sorround cubes
    xrange = (min(x[0] for x in input)-1, max(x[0] for x in input)+1)
    yrange = (min(x[1] for x in input)-1, max(x[1] for x in input)+1)
    zrange = (min(x[2] for x in input)-1, max(x[2] for x in input)+1)
    total = 0

    def in_range(pos):
        return xrange[0] <= pos[0] <= xrange[1] and \
            yrange[0] <= pos[1] <= yrange[1] and \
            zrange[0] <= pos[2] <= zrange[1]

    # explore all "air" cubes and keep track of how
    # often we touch a droplet cube using BFS
    pos = (xrange[0], yrange[0], zrange[0])
    q = deque([pos])
    visited = set([pos])
    while q:
        pos = q.popleft()
        for n in nei(pos):
            if n in input:
                total += 1
            elif n not in visited and in_range(n):
                q.append(n)
                visited.add(n)

    return total
    
print("Part 2:", part2())
# Part 2: 2546