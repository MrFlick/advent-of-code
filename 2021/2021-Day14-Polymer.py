from collections import Counter

sampleinput1 = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

lookup = dict()
#lines = iter(x.strip() for x in sampleinput1.split("\n"))
lines = iter(x.strip() for x in open("2021-Day14.txt").readlines())
for line in lines:
    if line == "": break
    start = line
for line in lines:
    pair, add = line.split(" -> ")
    lookup[pair] = add

pairs = Counter()
for i in range(len(start)-1):
    pairs[start[i:(i+2)]] += 1

def step(obs):
    result = Counter()
    for pair, count in obs.items():
        ele = lookup[pair]
        result[pair[0] + ele] += count
        result[ele + pair[1]] += count
    return result
    
print(pairs)
curr = pairs.copy()
for i in range(40):
    curr = step(curr)

def score(obs):
    elecount = Counter()
    for pair, count in obs.items():
        elecount[pair[0]] += count
        elecount[pair[1]] += count
    elecount[start[0]] += 1
    elecount[start[-1]] += 1
    cnts = sorted((x//2 for x in elecount.values()))
    return cnts[-1] - cnts[0]
print(score(curr))
