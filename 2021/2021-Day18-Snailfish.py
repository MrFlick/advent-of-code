
from functools import reduce

def parse_num(raw):
    stack = []
    idx = 0
    while idx < len(raw):
        if raw[idx] in ("[", ",", "]"):
            stack.append(raw[idx])
        else:
            num = int(raw[idx])
            while idx+1 < len(raw) and raw[idx+1].isdigit():
                idx += 1
                num = num*10 + int(raw[idx])
            stack.append(num)
        idx += 1
    return stack

def get_input(filename):
    inputs = []
    with open(filename) as f:
        for line in (x.strip() for x in f):
            inputs.append(parse_num(line))
    return inputs

def explode(snum):
    did_explode = False
    N = len(snum)
    depth = 0
    idx = 0
    lastnum = None
    passon = 0
    while idx < N:
        v = snum[idx] 
        if v == "[":
            depth += 1
            if depth == 5 and not did_explode:
                did_explode = True
                if lastnum is not None:
                    snum[lastnum] += snum[idx + 1]
                lastnum = idx
                passon = snum[idx + 3]
                del snum[idx:idx+4]
                snum[idx] = 0
                N -= 4
                depth == 4
                if passon == 0: break
        elif v == "]":
            depth -= 1
        elif v == ",":
            pass
        else: #number
            lastnum = idx
            if passon != 0:
                snum[idx] += passon
                passon = 0
                break
        idx += 1
    return did_explode

def split(snum):
    did_split = False
    N = len(snum)
    idx = 0
    while idx < N:
        v = snum[idx]
        if v in ('[', ',', ']'):
            pass
        else: #number
            if v >= 10:
                left = v // 2
                right = v - left
                snum[idx] = "]"
                snum.insert(idx, right)
                snum.insert(idx, ",")
                snum.insert(idx, left)
                snum.insert(idx, "[")
                N += 4
                did_split = True
                break
        idx += 1
    return did_split

def snumreduce(snum):
    actions = 1
    #print("i: ", end="")
    #psnum(snum)
    while(actions):
        actions = 0 
        while(explode(snum)):
            #print("e: ", end="")
            #psnum(snum)
            actions += 1
        if split(snum):
            #print("s: ", end="")
            #psnum(snum)
            actions += 1

def psnum(snum):
    print("".join(str(x) for x in snum))

def addsnum(a, b):
    snum = ["["] + a + [","] + b + ["]"]
    snumreduce(snum)
    return snum

def snummag(snum):
    q = []
    for v in snum:
        if v in ('[', ","):
            pass
        elif v == ']':
            q.append(q.pop()*2 + q.pop()*3)
        else:
            q.append(v)
    return q[0]

def best_sum(inputs):
    best = 0
    for i in range(len(inputs)-1):
        for j in range(i+1, len(inputs)):
            val1 = snummag(addsnum(inputs[i], inputs[j]))
            val2 = snummag(addsnum(inputs[j], inputs[i]))
            best = max(val1, val2, best)
    return best

inputs = get_input("2021-Day18.txt")
snum = inputs[0]
for i in range(1, len(inputs)):
    snum = addsnum(snum, inputs[i])
    #psnum(snum)

print(snummag(snum))
print(best_sum(inputs))