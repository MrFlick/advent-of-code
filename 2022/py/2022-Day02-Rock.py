

def norm_play(play):
    code = ord(play)-ord("A")
    if code > 3:
        code = code - 23
    # score, win_against, lose_against
    return (code+1, (code-1) % 3 + 1, (code-2) % 3 + 1)

def score_round_part1(them, me):
    them_throw, _, _ = norm_play(them)
    me_throw, me_win_against, _ = norm_play(me)
    score = me_throw
    if them_throw==me_throw:
        score += 3
    elif them_throw == me_win_against:
        score += 6
    return score

def score_round_part2(them, me):
    them_throw, them_win_against, them_lose_against = norm_play(them)
    if me ==  "X": #lose
        return them_win_against
    if me == "Y": #draw
        return them_throw + 3
    if me == "Z":
        return them_lose_against + 6


with open("2022-Day02.txt", encoding="utf-8") as f:
    score1 = 0
    score2 = 0
    for line in (x.strip() for x in f):
        (them, me) = line.split(" ")
        score1 += score_round_part1(them, me)
        score2 += score_round_part2(them, me)

print(score1)
#9759
print(score2)
#12429
