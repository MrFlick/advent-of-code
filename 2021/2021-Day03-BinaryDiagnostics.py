with open("2021-Day03.txt") as f:
    vals = [x.strip() for x in f]


def place1s(obs):
    ones = [0] * len(obs[0])
    for ob in obs:
        for i, c in enumerate(ob):
            if c=="1":
                ones[i] += 1
    return ones, len(obs)

def power(vals):
    pcount, N = place1s(vals)
    half = N//2
    gamma = 0
    epsilon = 0
    for c in pcount:
        gamma <<= 1
        epsilon <<= 1
        if c > half:
            gamma += 1
        else:
            epsilon += 1

    return gamma*epsilon, gamma, epsilon

def poscnt(vals, idx):
    onecnt = 0
    for v in vals:
        if v[idx]=="1":
            onecnt +=1
    return onecnt, len(vals) - onecnt

def o2(vals):
    vals = vals.copy()
    idx = 0
    while len(vals) > 1:
        c1, c0 = poscnt(vals, idx)
        if c0>c1:
            tgt = "0"
        else:
            tgt = "1"
        vals = list(filter(lambda x: x[idx]==tgt, vals))
        idx += 1
    return int(vals[0], base=2)

def co2(vals):
    vals = vals.copy()
    idx = 0
    while len(vals) > 1:
        c1, c0 = poscnt(vals, idx)
        if c1<c0:
            tgt = "1"
        else:
            tgt = "0"
        vals = list(filter(lambda x: x[idx]==tgt, vals))
        idx += 1
    return int(vals[0], base=2)

def life(vals):
    o2v = o2(vals)
    co2v = co2(vals)
    return o2v * co2v

print(power(vals))

print(life(vals))