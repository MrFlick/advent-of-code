import re
import math 

game_re = re.compile(r"Game (\d+)")
color_re = re.compile(r"(\d+) (red|green|blue)")

def parse_color(x):
    qty, color = color_re.findall(x)[0]
    return (int(qty), color)

def total_colors(x):
    result = {'red': 0, 'green': 0, 'blue': 0}
    for qty, color in x:
        result[color] += qty
    return result

def get_input(file):
    print(file)
    with open(file) as f:
        for line in f:
            raw_game, raw_draws = line.strip().split(":")
            game_id = int(game_re.findall(raw_game)[0])
            rounds = raw_draws.split(";")
            events = [ total_colors([parse_color(y)for y in x.split(",")]) for x in rounds]
            yield game_id, events

def is_possible(truth, test):
    for color, qty in truth.items():
        if test[color] > qty:
            return False
    return True

def min_set(events):
    result = {'red': 0, 'green': 0, 'blue': 0}
    for event in events:
        for color, qty in event.items():
            result[color] = max(result[color], qty)
    return result

def part1():
    truth = total_colors([(12, 'red'), (13, 'green'), (14, 'blue')])
    result = 0
    for game_id, events in get_input("2023-Day02.txt"):
        possible = True
        for event in events:
            if not is_possible(truth, event):
                possible = False
                break
        if possible:
            result += game_id
    return result

def part2():
    result = 0
    for game_id, events in get_input("2023-Day02.txt"):
        power = math.prod([x for x in min_set(events).values()])
        print(game_id, power)
        result += power
    return result

# 2003 - too low (had >= rather than >)
# 2369
print("part1", part1())

# 66363
print("part2", part2())
