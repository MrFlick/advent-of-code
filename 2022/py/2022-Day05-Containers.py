from collections import deque

with open ("2022-Day05.txt", encoding="utf-8") as f:
    rawstacks = []
    rowi = iter((x.strip('\n') for x in f.readlines()))
    while line := next(rowi):
        if line != "":
            rawstacks.append(line)
        else:
            break
    # process stacks
    ncols = (max(len(x) for x in rawstacks) + 1) //4
    p1_stacks = [deque() for i in range(ncols)]
    p2_stacks = [deque() for i in range(ncols)]
    for row in rawstacks[0:-1]:
        cols = [ row[i:(i+4)].strip(" []") for i in range(0, ncols*4, 4) ]
        for i,v in enumerate(cols):
            if v != "":
                p1_stacks[i].append(v)
                p2_stacks[i].append(v)
    for line in rowi:
        _, count, _, source, _, dest = line.split(" ")
        count = int(count)
        source = int(source)-1
        dest = int(dest)-1
        for i in range(count):
            p1_stacks[dest].appendleft(p1_stacks[source].popleft())
        move = [p2_stacks[source].popleft() for _ in range(count)]
        for c in reversed(move):
            p2_stacks[dest].appendleft(c)
    print("".join([x.popleft() for x in p1_stacks]))
    # CFFHVVHNC
    print("".join([x.popleft() for x in p2_stacks]))
    # FSZWBPTBG

