from heapq import heappush, heappop

def get_grid():
    with open("2022-Day12.txt", encoding="utf-8") as f:
        rows = [list(x.strip()) for x in f.readlines()]

    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if col.islower():
                rows[i][j] = ord(col)-96                
            elif col == "S":
                rows[i][j] = 1
                start = (i, j)
            elif col == "E":
                rows[i][j] = 26
                end = (i, j)
    return rows, start, end

dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
def nei(pos, NR, NC):
    for dx, dy in dirs:
        nextp = (pos[0] + dx, pos[1] + dy)
        if 0 <= nextp[0] < NR and 0 <= nextp[1] < NC:
            yield nextp

class PathFinderBase():

    def __init__(self):
        self.grid, self.sloc, self.eloc = get_grid()
        self.q = []
        self.visited = set()

    def init_search(self):
        raise NotImplementedError()

    def is_valid_move(self, pos, nextp):
        raise NotImplementedError()

    def is_solved(self, pos):
        raise NotImplementedError()

    def solve(self):
        NR = len(self.grid)
        NC = len(self.grid[0])
        self.init_search()
        while self.q:
            dist, pos = heappop(self.q)
            if self.is_solved(pos):
                return dist
            for nextp in nei(pos, NR, NC):
                if nextp not in self.visited:
                    if self.is_valid_move(pos, nextp):
                        self.visited.add(nextp)
                        heappush(self.q, (dist + 1, nextp))

class PathFinderPart1(PathFinderBase):
    def init_search(self):
        heappush(self.q, (0, self.sloc))
        self.visited.add(self.sloc)

    def is_valid_move(self, pos, nextp):
        return self.grid[nextp[0]][nextp[1]] <= self.grid[pos[0]][pos[1]] + 1

    def is_solved(self, pos):
        return pos == self.eloc

class PathFinderPart2(PathFinderBase):
    def init_search(self):
        heappush(self.q, (0, self.eloc))
        self.visited.add(self.eloc)

    def is_valid_move(self, pos, nextp):
        return self.grid[nextp[0]][nextp[1]] >= self.grid[pos[0]][pos[1]] - 1

    def is_solved(self, pos):
        return self.grid[pos[0]][pos[1]] == 1

print("Part 1:", PathFinderPart1().solve())
# 437
print("Part 2:", PathFinderPart2().solve())
# 430