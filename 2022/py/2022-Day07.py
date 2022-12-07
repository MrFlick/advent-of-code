from collections import defaultdict
import bisect
META = " ."
PARENT = f"{META}parent"
CSIZE = f"{META}csize"
DSIZE = f"{META}dsize"
MAXCAP = 70000000
NEEDEDCAP = 30000000

def dsize(folder: defaultdict):
    if DSIZE in folder:
        return folder[DSIZE]
    size = folder.get(CSIZE, 0)
    for k, v in folder.items():
        if k.startswith(META): continue
        if DSIZE in v:
            size += v[DSIZE]
        else:
            size += dsize(v)
    folder[DSIZE] = size
    return size

def find_dir_sizes(folder):
    yield dsize(folder)
    for k, v in folder.items():
        if k.startswith(META): continue
        yield from find_dir_sizes(v)

with open("2022-Day07.txt", encoding="utf-8") as f:
    lines = [x.strip() for x in f]
    line_index = 0
    def ddict():
        return defaultdict(ddict)
    fs = defaultdict(ddict)
    fs["/"][PARENT] = None
    current_path = fs["/"]
    while line_index < len(lines):
        line = lines[line_index]
        assert(line.startswith("$"))
        cmd = line.removeprefix("$ ").split(" ")
        if cmd[0] == "cd":
            if cmd[1] == "/":
                current_path = fs["/"]
            elif cmd[1] == "..":
                current_path = current_path[PARENT]
            else:
                parent = current_path
                current_path = current_path[cmd[1]]
                current_path[PARENT] = parent
        elif cmd[0] == "ls":
            line_index += 1
            current_size = 0
            while (line_index < len(lines) and not lines[line_index].startswith("$")):
                ls1, ls2 = lines[line_index].split(" ")
                if ls1 == "dir":
                    pass
                else:
                    fsize = int(ls1)
                    fname = ls2
                    current_size += fsize
                line_index += 1
            line_index -= 1
            current_path[CSIZE] = current_size
        line_index += 1

    dsizes = list(find_dir_sizes(fs["/"]))
    print("Part 1:", sum((x for x in dsizes if x<100000)))
    dsizes.sort()
    need = NEEDEDCAP - (MAXCAP-dsize(fs["/"]))
    print("Part 2:", dsizes[bisect.bisect_left(dsizes, need)])