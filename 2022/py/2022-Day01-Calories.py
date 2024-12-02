
elves = []

with open("2022-Day01.txt", encoding="utf-8") as f:
    current_elf = 0
    for line in f:
        line = line.strip()
        if line == "":
            elves.append(current_elf)
            current_elf = 0
        else:
            current_elf += int(line)
elves.append(current_elf)

elves.sort(reverse=True)
print(elves[0])
print(sum(elves[0:3]))
        
