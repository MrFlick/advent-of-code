from collections import Counter


# Rather than tracking position as 1-10, use 0-9
with open("2021-Day21.txt") as f:
    pos = [int(x.strip().split(": ")[1])-1 for x in f.readlines()]

def num10(x): return x % 10 + 1

def get_roll():
    def num100(x): return x % 100 + 1
    i=0
    while True:
        yield num100(i) + num100(i+1) + num100(i+2)
        i = (i + 3) % 100

def get_outcome(pos, win=1000):
    score = [0,0]
    rolls = 0
    dice = get_roll()

    def take_turn(p, win):
        nonlocal rolls
        d = next(dice)
        rolls += 1
        pos[p] += d
        pos[p] %= 10
        score[p] += num10(pos[p])
        if score[p] >= win:
            return True
        return False

    while True:
        did_win = take_turn(0, win=win)
        if did_win:
            break
        did_win = take_turn(1, win=win)
        if did_win:
            break
    
    return(rolls*3 * min(score))

print(get_outcome(pos))

# wts are often each value 0-9 occur when you roll 3, 3-sided dice
wts = [0,0,0,1,3,6,7,6,3,1]
WIN_SCORE = 21
def sim(pos, score=0, turns = 1, wt = 1, counts = None, path = None):
    """This function calculates the number of time a player would 
    win for a certain number of turns"""
    if counts is None:
        counts = [0]*13
    if path is None:
        path = []
    for move in range(3, 10):
        land = (pos + move) % 10
        path.append(move)
        if score + land + 1 >= WIN_SCORE:
            counts[turns] += wt * wts[move]
            #if turns == 2:
            #    print(wt*wts[move], path)
        else:
            sim(land, score+land+1, turns+1, wt * wts[move], counts=counts, path=path)
        path.pop()
    return counts

p1w = sim(pos[0])
p2w = sim(pos[0])

win1 = 0
u1 = 1
win2 = 0
u2 = 1
p2w[10] = 0

for i in range(1, len(p1w)):
    u1 *= 3**3
    if p1w[i] > 0:
        win1 += p1w[i] * u2
        u1 -= p1w[i]
    u2 *= 3**3
    if p2w[i] > 0:
        win2 += p2w[i] * u1
        u2 -= p2w[i]

# u1 should be 0 (all universes used up)

print("e {:,}".format(win1))
print("e {:,}".format(win2))


