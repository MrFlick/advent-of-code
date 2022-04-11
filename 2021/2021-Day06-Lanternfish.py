
with open("2021-Day06.txt") as f:
    fish = [int(x) for x in f.read().strip().split(",")]

def collapse(fish):
    r = [0] * 9
    for v in fish:
        r[v] += 1
    return r

def step(counts):
    ones = counts[0]
    for i in range(1, len(counts)):
        counts[i-1] = counts[i]
    counts[8] = ones
    counts[6] += ones

obs = collapse(fish)
for _ in range(256):
    step(obs)

print(sum(obs))
