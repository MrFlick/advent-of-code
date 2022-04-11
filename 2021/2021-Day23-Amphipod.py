EMPTY = "."

def get_puzzle(filename):
    state = [EMPTY] * 15
    with open(filename) as f:
        rows = f.readlines()
    for i, c in enumerate((3, 5, 7, 9)):
        state[i*2+7] = rows[2][c]
        state[i*2+8] = rows[3][c]
    return state

# Positions:
#
# 00  01  02  03  04  05  06
#       07  09  11  13
#       08  10  12  14
#

pathtoroom = {
    (0, 0): (1,- 1), (0, 1): (1, -1, 2, -1), (0, 2): (1, -1, 2, -1, 3, -1), (0, 3): (1, -1, 2, -1, 3, -1, 4, -1),
    (1, 0): (-1,), (1, 1): (-1, 2, -1), (1, 2): (-1, 2, -1, 3, -1), (1, 3): (-1, 2, -1, 3, -1, 4, -1),
    (2, 0): (-1,), (2, 1): (-1,), (2, 2): (-1, 3, -1), (2, 3): (-1, 3,-1, 4, -1),
    (3, 0): (-1, 2, -1), (3, 1): (-1,), (3, 2): (-1, ), (3, 3): (-1, 4, -1),
    (4, 0): (-1, 3,-1, 2, -1), (4, 1): (-1, 3, -1), (4, 2): (-1,), (4, 3): (-1,),
    (5, 0): (-1, 4, -1, 3,-1, 2, -1), (5, 1): (-1, 4, -1, 3, -1), (5,2): (-1, 4, -1), (5, 3): (-1,),
    (6, 0): (5,-1, 4,-1, 3,-1, 2, -1), (6, 1): (5,-1, 4,-1, 3, -1), (6,2): (5,-1, 4, -1), (6, 3): (-1, 5,-1)
}
pathtohall = {
    0: ((-1, 1, -1, 0), (-1, 2, -1, 3, -1, 4, -1, 5, 6)),
    1: ((-1, 2, -1, 1, 0), (-1, 3, -1, 4, -1, 5, 6)),
    2: ((-1, 3, -1, 2, -1, 1, 0), (-1, 4, -1, 5, 6)),
    3: ((-1, 4, -1, 3, -1, 2, -1, 1, 0), (-1, 5, 6))
}
roomtoroom = {
    (0, 1): (-1, 2, -1), (0, 2): (-1, 2, -1, 3, -1), (0, 3): (-1, 2, -1, 3, -1, 4, -1), 
    (1, 0): (-1, 2, -1), (1, 2): (-1, 3, -1), (1, 3): (-1, 3, -1, 4, -1), 
    (2, 0): (-1, 3, -1, 2, -1), (2, 1): (-1, 3, -1), (2, 3): (-1, 4, -1), 
    (3, 0): (-1, 4, -1, -3, -1, 2, -1), (3, 1): (-1, 4, -1, -3, -1), (3, 2): (-1, 4, -1)
}

def possmoves(pos, state, target):
    poss = []
    atype = state[pos]
    if atype==EMPTY: return []
    if pos <=6: #outside
        room = target.index(atype)
        if state[room*2+7] != EMPTY: return []
        path = pathtoroom[(pos, room)]
        if state[room*2+7] == EMPTY:
            if state[room*2+7+1] == EMPTY:
                path += (room*2+7, room*2+7+1)
            elif state[room*2+7+1] != atype:
                return []
            else:
                path += (room*2+7,)
        else:
            return []
        dist = 1
        for space in path:
            if space == -1 or state[space] == EMPTY:
                if space == path[-1]:
                    poss.append((space, dist*costs[atype]))
                dist += 1
            else:
                break
        return poss
    else: #inside
        room = (pos-7)//2
        targetroom = target.index(atype)
        isback = pos > room*2+7
        if isback and (room == targetroom or state[room*2+7] != EMPTY):
            return [] #either blocked or already correct
        if (room == targetroom and state[pos+1]==atype):
            return [] #room already correct
        for end in pathtohall[room]:
            dist = 2 if isback else 1
            for space in end:
                if space == -1 or state[space] == EMPTY:
                    if 0 <= space <= 6:
                        poss.append((space, dist*costs[atype]))
                    dist += 1
                else: 
                    break
        if room != targetroom:
            path = roomtoroom[(room, targetroom)]
            if state[targetroom*2+7] == EMPTY:
                if state[targetroom*2+7+1] == EMPTY:
                    path += (targetroom*2+7, targetroom*2+7+1)
                elif state[targetroom*2+7+1] == atype:
                    path += (targetroom*2+7,)
                else:
                    path = tuple()
            else:
                path = tuple()
            dist = 2 if isback else 1
            for space in path:
                if space == -1 or state[space] == EMPTY:
                    if space == path[-1]:
                        poss.append((space, dist*costs[atype]))
                    dist += 1
                else: 
                    break
        return poss


costs = {"A": 1, "B": 10, "C": 100, "D":1000}
pz = get_puzzle("2021-Day23.txt")
print(pz)

def iswin(state, target):
    for i, v in enumerate(target):
        if state[i*2+7] != v: return False
        if state[i*2+7+1] != v: return False
    return True

cache = dict()
gbest = None
def search(state, target=("A", "B", "C", "D"), cost=0):
    global gbest
    key = "".join(state)
    if key in cache:
        if cache[key] is None:
            return False, 0
        elif cost >= cache[key]:
            return True, cache[key]
    if gbest is not None and cost > gbest:
        cache[key] = None
        return False, 0
    if iswin(state, target):
        cache[key] = cost
        if gbest is None or cost < gbest:
            gbest = cost
        print(key, cost)
        return True, cost
    #print(key, cost)
    best = None
    foundwin = False
    foundmove = False
    for i in range(0, 15):
        poss = possmoves(i, state, target)
        for space, spacecost in poss:
            foundmove = True
            person = state[i]
            state[i] = EMPTY
            state[space] = person
            didwin, pathcost = search(state, target, cost+spacecost)
            state[i] = person
            state[space] = EMPTY
            if didwin:
                foundwin = True
                if best is None or pathcost < best:
                    best = pathcost
    if not foundmove:
        return False, 0
    cache[key] = best
    return foundwin, best
search(pz)