from collections import Counter

list1 = []
list2 = []

with open("2024-Day01.txt") as f:
    for line in f:
        a, b = line.strip().split()
        list1.append(int(a))
        list2.append(int(b))

list1.sort()
list2.sort()

cnt = Counter(list2)

result1 = 0
result2 = 0
for (a,b) in zip(list1, list2):
    result1 += abs(a-b)
    result2 += a * cnt[a]

print("Part 1: ", result1)
# 1660292
print("Part 2: ", result2)
# 22776016