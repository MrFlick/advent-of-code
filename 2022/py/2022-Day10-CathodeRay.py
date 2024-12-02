with open("2022-Day10.txt") as f:
    ops = [x.strip().split() for x in f.readlines()]

def cycles() :
    yield 0
    for op in ops:
        if op[0] == "noop":
            yield 0
        elif op[0] == "addx":
            yield 0
            yield int(op[1])

def register_values():
    x = 1
    for d in cycles():
        x += d
        yield x

signal_strength = 0
for i, reg in enumerate(register_values()):
    cycle = i + 1
    if cycle in [20, 60, 100, 140, 180, 220]:
        #print(cycle, ": ", cycle * reg, " ", reg)
        signal_strength += cycle * reg
print("Part 1:", signal_strength)
# 15260

screen = [["."] * 40 for _ in range(6) ]

def print_screen(screen):
    for row in screen:
        print("".join(row))

for i, reg in enumerate(register_values()):
    pos = i%40
    if pos-1 <= reg <= pos+1:
        screen[i // 40][pos] = "#"

print_screen(screen)
# PGHFGLUG