with open("2022-Day09.txt") as f:
    moves = [ (x[0], int(x[1])) for x in [line.strip().split(" ") for line in f]]

delta = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}

def init_rope(length):
    return [ (0,0) for _ in range(length)]

def must_move_knot(head, tail):
    return not(abs(head[0]-tail[0])<=1 and abs(head[1]-tail[1]) <=1)

def move_head(head, dir):
    d = delta[dir]
    return((head[0] + d[0], head[1] + d[1]))

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def adjust_tail(head, tail):
    x = tail[0] + sign(head[0]-tail[0])
    y = tail[1] + sign(head[1]-tail[1])
    return (x, y)

def simulate_rope(moves, rope):
    visited = set([rope[-1]])

    for dir, dist in moves:
        for _ in range(dist):
            rope[0] = move_head(rope[0], dir)
            for i in range(1, len(rope)):
                if must_move_knot(rope[i-1], rope[i]):
                    rope[i] = adjust_tail(rope[i-1], rope[i])
            visited.add(rope[-1])

    return len(visited)

print("Part 1", simulate_rope(moves, init_rope(2)))
# Part 1 6376
print("Part 2", simulate_rope(moves, init_rope(10)))
# Part 2 2607
            


