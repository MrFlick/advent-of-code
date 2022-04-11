
with open("2021-Day01.txt") as f:
    obs = [int(x) for x in f.readlines()]

inc = 0
for i in range(1, len(obs)):
    inc += obs[i] > obs[i-1]

print(inc)

inc = 0
win = 3

val = sum(obs[0:win])
last = val

for i in range(win, len(obs)):
    val = val + obs[i] - obs[i-win]
    if val > last:
        inc += 1
    last = val

print(inc)