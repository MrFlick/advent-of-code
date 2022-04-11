with open("2021-Day07.txt") as f:
    crabs = [int(x) for x in f.read().strip().split(",")]
    crabs.sort()



def tri(x):
    return x * (x+1) // 2

best = None
bestpos = None
for pos in range(crabs[0], crabs[-1]+1):
    total = sum(abs(c - pos) for c in crabs)
    if best is None or total < best:
        best = total
        bestpos = pos

print(best, bestpos)


best = None
bestpos = None
for pos in range(crabs[0], crabs[-1]+1):
    total = sum(tri(abs(c - pos)) for c in crabs)
    if best is None or total < best:
        best = total
        bestpos = pos

print(best, bestpos)

