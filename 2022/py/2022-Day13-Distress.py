import functools
sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def parse_list(line):
    # return eval(line)
    # build a parser rather than using built in python parser
    result = []
    q = []
    q.append(result)
    current = result
    hasval = False
    val = 0
    for char in line:
        if char == "[":
            current = []
            q.append(current)
        elif char == "]":
            if hasval:
                current.append(val)
            part = q.pop()
            current = q[-1]
            current.append(part)
            hasval = False
            val = 0
        elif char == ",":
            if hasval:
                current.append(val)
            hasval = False
            val = 0
        else:
            hasval = True
            val = val * 10 + int(char)
    return result[0]

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return sign(a-b)
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    for i in range(min(len(a), len(b))):
        cmp =  compare(a[i], b[i])
        if cmp != 0:
            return cmp
    return sign(len(a) - len(b))
    
with open("2022-Day13.txt") as f:
    content = f.read()
    groups = map(lambda x: x.split("\n"), content.split("\n\n"))
    result = 0
    for i, (a, b) in enumerate(groups):
        if compare(parse_list(a), parse_list(b)) == -1:
            result += i+1
    print("Part 1: ", result)

with open("2022-Day13.txt") as f:
    entries = [parse_list(x.strip()) for x in f.readlines() if x.strip()]
    entries.append([[2]])
    entries.append([[6]])
    entries.sort(key=functools.cmp_to_key(compare))
    result = 1
    for i, e in enumerate(entries):
        if compare(e, [[2]]) == 0:
            result *= i+1
        if compare(e, [[6]]) == 0:
            result *= i+1
    print("Part 2: ", result)
    
    




