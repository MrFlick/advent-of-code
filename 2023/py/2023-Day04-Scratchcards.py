import re

def get_input(path):
    with open(path) as f:
        for line in f:
            label, data = line.strip().split(":")
            winners, picked = data.split("|")
            winners = [int(x) for x in re.split(r"\s+", winners.strip())]
            picked = [int(x) for x in re.split(r"\s+", picked.strip())]
            card = int(label.removeprefix("Card"))
            yield card, winners, picked

def match_card(winners, picks):
    winners = set(winners)
    matches = sum(x in winners for x in picks)
    return matches

def score_card(matches):
    if matches < 1:
        return 0
    return 2**(matches-1)

def base_match_cards(data):
    return [match_card(winners, picks) for _, winners, picks in data]

def deep_score_cards(data):
    scores = base_match_cards(data)
    for i in reversed(range(len(scores))):
        if scores[i] == 0:
            continue
        for j in range(i+1, i+scores[i]+1):
            scores[i] += scores[j]
    return scores

def part1():
    data = get_input("2023-Day04.txt")
    total = sum(score_card(matches) for matches in base_match_cards(data))
    return total

def part2():
    grid = get_input("2023-Day04.txt")
    scores = deep_score_cards(grid)
    return sum( 1 + x for x in scores)

# 28750
print("part1:", part1())

# 10212704
print("part2:", part2())