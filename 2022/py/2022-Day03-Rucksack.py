def priority(val):
    val = ord(val)
    if val < ord('a'):
        return val - ord('A') + 27
    else:
        return val - ord('a') + 1
    

with open("2022-Day03.txt", encoding="utf-8") as f:
    p1total = 0
    p2total = 0
    idx = 0
    group = set()
    for line in (x.strip() for x in f):
        size = len(line)//2
        a = set(line[0:size])
        b = set(line[size:])
        if idx == 0:
            group = set(line)
        else:
            group = group.intersection(set(line))
        if idx == 2:
            p2total += priority(list(group)[0])
        shared = list(a.intersection(b))[0]
        p1total += priority(shared)
        idx = (idx + 1) % 3
    print(p1total)
    # 8394
    print(p2total)
    # 2413
    