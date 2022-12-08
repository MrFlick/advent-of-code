with open("2022-Day08.txt") as f:
    grid = [[int(x) for x in row.strip()] for row in f.readlines()]
    NR, NC = len(grid), len(grid[0])
    vis = [[0 for _ in range(NC)] for _ in range(NR)]
    
    def gget(pos):
        return grid[pos[0]][pos[1]]
    def vinc(pos):
        vis[pos[0]][pos[1]] += 1

    def gridsweep(majrange, minrange, topos, size):
        sweep = [0] * size
        for major in majrange:
            for minor in minrange:
                pos = topos(major, minor)
                if major == 0:
                    sweep[minor] = gget(pos)
                    vinc(pos)
                else:
                    if gget(pos) > sweep[minor]:
                        vinc(pos)
                        sweep[minor] = gget(pos)

    gridsweep(range(NR), range(NC), lambda x, y: (x, y), NC)
    gridsweep(range(NR), range(NC), lambda x, y: (NR-x-1, y), NC)
    gridsweep(range(NC), range(NR), lambda x, y: (y, x), NR)
    gridsweep(range(NC), range(NR), lambda x, y: (y, NC-x-1), NR)
    
    print("Part 1: ", sum(sum(x>0 for x in row) for row in vis))
    # 1647

    def score(vals):
        out = [0] * len(vals)
        for i in range(1, len(vals)):
            start = vals[i]
            for j in range(i-1, -1, -1):
                if vals[j] >= start:
                    out[i] += 1
                    break
                else:
                    out[i] += 1
        return out

    lookL = [score(row) for row in grid]
    lookR = [list(reversed(score(list(reversed(row))))) for row in grid]
    lookU = [score([grid[r][c] for r in range(NR)]) for c in range(NC)]
    lookD = [list(reversed(score([grid[NR-r-1][c] for r in range(NR)]))) for c in range(NC)]

    maxscore = 0
    for r in range(NR):
        for c in range(NC):
            score = lookL[r][c] * lookR[r][c] * lookU[c][r] * lookD[c][r]
            if score > maxscore:
                maxscore = score
    print("Part 2: ", maxscore)
    
    # 450 too low
    # 2160 too low
    # 392080