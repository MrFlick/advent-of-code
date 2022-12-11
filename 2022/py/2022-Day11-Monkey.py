from collections import deque
from math import floor, prod

class Monkey():
    def __init__(self, items, obsfn, divby, iftrue, iffalse):
        self.items = deque(items)
        self.obsfn = obsfn
        self.divby = divby
        self.iftrue = iftrue
        self.iffalse = iffalse

    def inspect(self, adjust):
        while self.items:
            item = self.items.popleft()
            val = self.obsfn(item)
            val = adjust(val) 
            if val % self.divby == 0:
                yield(self.iftrue, val)
            else:
                yield(self.iffalse, val)

    def receive(self, val):
        self.items.append(val)

    @staticmethod
    def parse(rows: list[str]):
        items = [int(x) for x in rows[1].removeprefix("Starting items:").split(", ")]        
        obsfn = toobfn(rows[2])
        divby = int(rows[3].removeprefix("Test: divisible by "))
        iftrue = int(rows[4].removeprefix("If true: throw to monkey "))
        iffalse = int(rows[5].removeprefix("If false: throw to monkey "))
        return Monkey(items, obsfn, divby, iftrue, iffalse)

def toobfn(row):
    op = row.removeprefix("Operation: new = ").split(" ")
    def obs(x):
        a = x if op[0]=="old" else int(op[0])
        b = x if op[2]=="old" else int(op[2])
        return {"*": a*b, "+": a+b}[op[1]]
    return obs

def get_monkeys() -> list[Monkey]:
    monkeys = []
    with open ("2022-Day11.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        for i in range(0, len(lines)+1, 7):
            monkeys.append(Monkey.parse(lines[i:(i+6)]))
    return monkeys

def run_simulation(part):
    monkeys = get_monkeys()
    if part == 1:
        N = 20
        adjust = lambda x: floor(x/3)
    elif part == 2:
        N = 1000
        # the secret here is to divide all numbers by 
        # by the least common multiple (or just a multiple)
        # of each of the div test so numbers don't explode
        cap = prod(m.divby for m in monkeys)
        adjust = lambda x: x % cap
    
    minspect = [0] * len(monkeys)
    for _ in range(N):
        for i, m in enumerate(monkeys):
            for toss, item in m.inspect(adjust):
                minspect[i] += 1
                monkeys[toss].receive(item)
    return(prod(sorted(minspect, reverse=True)[0:2]))


print("Part 1", run_simulation(1))
print("Part 2", run_simulation(2))

# Part 1 120056
# Part 2 218950768