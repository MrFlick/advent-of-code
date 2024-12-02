def is_safe_inner(levels: list[int], decreasing: bool = False, allowed_bad: int = 0, a=0, b=1, c=2) -> bool:

    def diff_ok(x, y, decreasing):
        d = y - x
        if decreasing:
            d = -d
        return 1 <= d <= 3
    
    if len(levels) < 2:
        return True
    if len(levels) < 3:
        return diff_ok(levels[a], levels[b], decreasing) or allowed_bad > 0
    while c < len(levels):
        if diff_ok(levels[a], levels[b], decreasing) and diff_ok(levels[b], levels[c], decreasing):
            (a, b, c) = (b, c, c+1)
            continue
        elif allowed_bad > 0:
            allowed_bad -= 1
            return is_safe_inner(levels, decreasing=decreasing, allowed_bad=0, a=b, b=c, c=c+1) or \
                is_safe_inner(levels, decreasing=decreasing, allowed_bad=0, a=a, b=c, c=c+1) or \
                is_safe_inner(levels, decreasing=decreasing, allowed_bad=0, a=a, b=b, c=c+1)
        else:
            return False
    return True

def is_safe_one(levels):
    return is_safe_inner(levels, False)  or is_safe_inner(levels, True)

def is_safe_two(levels):
    return is_safe_inner(levels, False, 1)  or is_safe_inner(levels, True, 1)


with open("2024-Day02.txt") as f:
    result1 = 0
    result2 = 0
    for line in f:
        levels = [int (x) for x in line.strip().split()]
        if is_safe_one(levels):
            result1 += 1
        if is_safe_two(levels):
            result2 += 1

print("Part 1: ", result1)
# 421
print("Part 2: ", result2)
# 476

print(is_safe_two([1,9]))