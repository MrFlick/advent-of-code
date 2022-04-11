from collections import deque
from copy import deepcopy

test = [[1,1,1,1,1],[1,9,9,9,1], [1,9,1,9,1], [1,9,9,9,1], [1,1,1,1,1]]
sample = [[int(y) for y in list(x.strip())] for x in open("2021-Day11.txt").readlines()]

def nei(r, c, board):
    R = len(board)
    C = len(board[0])
    for dr, dc in ((1,1),(1,0), (1,-1), (0,1), (0, -1), (-1,1), (-1,0), (-1, -1)):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < R and 0 <= nc < C:
            yield nr, nc


def grow(board, flashed, r, c):
    q = deque()
    q.append((r,c))
    while q:
        r, c = q.popleft()
        if flashed[r][c]: continue
        flashed[r][c] = True
        board[r][c] = 0
        for nr, nc in nei(r, c, board):
            if flashed[nr][nc]: continue
            board[nr][nc] += 1
            if board[nr][nc] > 9:
                q.append((nr, nc))

def step(board):
    R = len(board)
    C = len(board[0])
    flashed = [[False] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if flashed[r][c]: continue
            board[r][c] += 1
            if board[r][c] > 9:
                grow(board, flashed, r, c)
    return sum([sum(row) for row in flashed])

def run_steps(board, n):
    total = 0
    for _ in range(n):
        total += step(board)
    return total

def first_sync(board):
    N = len(board) * len(board[0])
    x = 0
    i = 0
    while x != N:
        x = step(board)
        i += 1
    return i


print(run_steps(deepcopy(sample), 100))

print(first_sync(deepcopy(sample)))



