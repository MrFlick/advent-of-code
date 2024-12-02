from dataclasses import dataclass

@dataclass
class Digit:
    value: int
    pos: int

def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        return [ int(x) for x in f.readlines()]

def get_dest(start, delta, mod):
    # Calcuating the destination point is odd
    # because it doesn't seem like anything can get shifted
    # to the 0 index, so we drop the first spot and return a
    # an index into the remaining lots (1..N-1 rather than 0..N-1)
    if delta == 0:
        return start
    return (start + delta - 1) % (mod-1) + 1

def unmix(digits, times = 1):
    # keep elements in original order
    # and tracks current pos(ition)/index
    # shifting an element involved changing the
    # positions between the starting pos and
    # destination pos
    digits = [ Digit(x, i) for i, x in enumerate(digits)]
    for _ in range(times):
        for d in digits:
            dest = get_dest(d.pos, d.value, len(digits))
            if dest == d.pos:
                pass
            elif dest < d.pos:
                for o in digits:
                    if dest <= o.pos < d.pos:
                        o.pos += 1
                d.pos = dest
            else:
                for o in digits:
                    if d.pos < o.pos <= dest:
                        o.pos -= 1
                d.pos = dest            
    x = [x for x in digits]
    x.sort(key=lambda x: x.pos)
    return [d.value for d in x]

def score(digits):
    zeroat = digits.index(0)
    return sum([digits[(zeroat + i) % len(digits)] for i in (1000, 2000, 3000)])


digits = get_input("2022-Day20.txt")
print("Part 1:", score(unmix(digits)))
# 9029 (too low)
# Part 1: 17490

key = 811589153
digits = [key * x for x in digits]
print("Part 2:", score(unmix(digits, times=10)))
# Part 2: 1632917375836
