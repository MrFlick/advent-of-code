from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush


def from_back(input):
    N = len(input)
    i = N-2 if N % 2 == 0 else N-1
    while i >= 0:
        val = int(input[i])
        for r in range(val):
            pos = yield((i//2, val-r-1))
        i -= 2

def from_back2(input):
    N = len(input)
    i = N-2 if N % 2 == 0 else N-1
    while i >= 0:
        val = int(input[i])
        yield((i//2, val))
        i -= 2

def spaces(input):
    N = len(input)
    i = 0
    is_file = True
    idx = 0
    while 0 <= i < N:
        val = int(input[i])
        if not is_file:
            yield (idx, val)
        idx += val
        is_file = not is_file
        i += 1

def ffiles(input):
    N = len(input)
    i = 0
    is_file = True
    idx = 0
    while 0 <= i < N:
        val = int(input[i])
        if not is_file:
            yield (idx, val)
        idx += val
        is_file = not is_file
        i += 1


def part1(filename):
    with open(filename) as f:
        input = f.readline().strip()
    fillers = iter(from_back(input))
    result = 0
    input_index = 0
    output_index = 0
    last_fill = None
    while input_index < len(input): 
        value = int(input[input_index])
        for r in range(value):
            current = (input_index//2, r)
            if last_fill is not None and current >= last_fill:
                break
            result += current[0] * output_index
            output_index += 1
            last = current
        input_index += 1
        if input_index >= len(input):
            break
        value = int(input[input_index])
        for r in range(value):
            filler = next(fillers)
            if filler > last:
                result +=  filler[0] * output_index
                last_fill = filler
                output_index += 1
            else:
                break
        input_index += 1
    return result

print("Part 1: ", part1("2024-Day09.txt"))
# 6353658451014

@dataclass
class FileEvent:
    start: int
    width: int

    def __lt__(self, other):
        return (self.start, self.width) < (other.start, other.width)

@dataclass
class DataFile(FileEvent):
    id: int

@dataclass
class FreeSpace(FileEvent):
    pass
    

def get_input2(filename):
    with open(filename) as f:
        input = f.readline().strip()
    N = len(input)
    i = 0
    is_file = True
    idx = 0
    files: list[DataFile] = []
    spaces = defaultdict(list)
    while 0 <= i < N:
        val = int(input[i])
        if val > 0:
            if is_file:
                files.append(DataFile(idx, val, i//2))
            else:
                heappush(spaces[val], FreeSpace(idx, val))
        idx += val
        is_file = not is_file
        i += 1
    return files, spaces

def part2(filename):
    files, spaces = get_input2(filename)

    for file in reversed(files):
        best: FreeSpace | None = None
        for i in range(file.width, 10):
            if len(spaces[i]):
                consider = heappop(spaces[i])
                if consider.start > file.start:
                    # put back
                    heappush(spaces[i], consider)
                    continue
                if best is None:
                    best = consider
                elif consider.start < best.start:
                    heappush(spaces[best.width], best)
                    best = consider
                else:
                    # put back
                    heappush(spaces[i], consider)
        if best is not None:
            if best.width > file.width:
                heappush(spaces[best.width - file.width], FreeSpace(best.start + file.width, best.width - file.width))
            file.start = best.start
    # checksum
    result = 0
    for file in files:
        for i in range(file.width):
            result += (file.start + i) * file.id
    return result


print("Part 2: ", part2("2024-Day09.txt"))
# 6382582136592
