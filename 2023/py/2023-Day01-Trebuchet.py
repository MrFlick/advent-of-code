
def get_input(file):
    with open(file) as f:
        return f.read().splitlines()
    
digit_names = ('zero ','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    
def first_last_digit(x: str):
    first, last = "",""
    for c in x:
        if c.isdigit():
            if not first:
                first = c
            last = c
    return int(first), int(last)

def number_at_index(x: str, i: int):
    if x[i].isdigit():
        return int(x[i])
    for digit_val, digit_name in enumerate(digit_names):
        if x[i:].startswith(digit_name):
            return digit_val
    return None

def first_number(x: str):
    i = 0
    while i < len(x):
        digit = number_at_index(x, i)
        if digit is not None:
            return digit
        i += 1
    raise Exception("First number not found")
        
def last_number(x: str):
    i = len(x)-1
    while i >= 0:
        digit = number_at_index(x, i)
        if digit is not None:
            return digit
        i -= 1
    raise Exception("Last number not found")


def first_last_number(x: str):
    first = first_number(x)
    last = last_number(x)
    return (first, last)

def part1():
    total = 0
    #lines = get_input("2023-Day01-test1.txt")
    lines = get_input("2023-Day01.txt")
    for x in lines:
        first, last = first_last_digit(x)
        total += first*10 + last
    return(total)

def part2():
    total = 0
    #lines = get_input("2023-Day01-test2.txt")
    lines = get_input("2023-Day01.txt")
    for x in lines:
        first, last = first_last_number(x)
        total += first*10 + last
    return(total)

# 53651 correct
print("part1", part1())

# 53896 too high
# twone should be 2 and 1 (overlaps are ok)
# 53894 correct
print("part2", part2())
