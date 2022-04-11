

with open("2021-Day10.txt") as f:
    lines = [x.strip() for x in f.readlines()]

pairs = {"{": "}", "(": ")", "<": ">", "[": "]"}
cx_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
ix_scores = {")": 1, "]": 2, "}": 3, ">": 4}

def score_corrutpted(char):
    return cx_scores[char]

def score_incomplete(q):
    score = 0
    for c in reversed(q):
        score = score * 5 + ix_scores[pairs[c]]
    return score


def check(line):
    q = []
    for idx, c in enumerate(line):
        if c in pairs:
            q.append(c)
        elif q and pairs[q[-1]] == c:
            q.pop()
        else:
            return "cx", score_corrutpted(c)
    if q:
        return "ix", score_incomplete(q)
    return "ok", 0

total_score = 0
for line in lines:
    result, score = check(line)
    if result == "cx":
        total_score += score
print(total_score)


total_score = 0

scores = [y for x, y in (check(line) for line in lines) if x=="ix"]
scores.sort()
print(scores[len(scores)//2])
    


