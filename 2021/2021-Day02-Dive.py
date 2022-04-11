
commands = []
with open("2021-Day02.txt") as f:
    for line in f:
        dir, dist = line.strip().split(" ")
        commands.append((dir, int(dist)))

h = 0
d = 0

for dir, dist in commands:
    if dir == "forward":
        h += dist
    elif dir == "down":
        d += dist
    elif dir == "up":
        d -= dist
    else:
        print("err")

print(h * d)


h = 0
d = 0
aim = 0

for dir, dist in commands:
    if dir == "forward":
        h += dist
        d += dist * aim
    elif dir == "down":
        aim += dist
    elif dir == "up":
        aim -= dist
    else:
        print("err")

print(h * d)