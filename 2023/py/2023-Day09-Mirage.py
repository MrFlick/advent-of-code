from typing import List


def get_input(path):
    with open(path) as f:
        return [[int(y) for y in x.strip().split(" ")] for x in f.readlines()]

def diffs(seq: List[int]):
    return [y-x for x,y in zip(seq[:-1], seq[1:])]

def pred_next(seq: List[int]):
    d = diffs(seq)
    if all(x==0 for x in d):
        return seq[-1]
    else:
        return seq[-1] + pred_next(d)
    
def pred_prev(seq: List[int]):
    d = diffs(seq)
    if all(x==0 for x in d):
        return seq[0]
    else:
        return seq[0] - pred_prev(d)
    
def part1():
    input = get_input("2023/py/2023-Day09.txt")
    total = sum(pred_next(seq) for seq in input)
    return total

def part2():
    input = get_input("2023/py/2023-Day09.txt")
    total = sum(pred_prev(seq) for seq in input)
    return total

# 1806615041
print("part1: ", part1())

# 1211
print("part2: ", part2())