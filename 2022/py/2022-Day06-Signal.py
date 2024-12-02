def find_first(x, size=4):
    i = 4
    c = x[0:size]
    while len(set(c))!=size:
        c = c[1:] + x[i]
        i += 1
    return i

with open("2022-Day06.txt") as f:
    for line in f:
        print(find_first(line))
        print(find_first(line, 14))
