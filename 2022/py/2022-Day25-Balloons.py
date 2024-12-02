def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        lines = [x.strip() for x in f.readlines()]
    return lines

def snafu2dec(num):
    digits = reversed(list(num))
    power = 0
    output = 0
    for d in digits:
        if d == "2":
            output += 2 * 5**power
        elif d=="1":
            output += 1 * 5**power
        elif d == "0":
            pass
        elif d == "-":
            output -= 1 * 5**power
        elif d == "=":
            output -= 2 * 5**power
        power += 1
    return output

places = ("=","-","0","1","2")
def dec2snafu(num):
    digits = []
    while num != 0:
        shift = ((num % 5) + 2) % 5
        digits.append(places[shift])
        num = num - (shift-2)
        num //= 5
    return "".join(reversed(digits))


def part1():
    numbers = get_input("2022-Day25.txt")
    total = sum(snafu2dec(num) for num in numbers)
    return dec2snafu(total)

print("Part 1:", part1())
# Part 1: 20=2-02-0---02=22=21