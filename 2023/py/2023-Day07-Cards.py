from dataclasses import dataclass
from collections import Counter
from typing import List


@dataclass
class Hand:
    cards: str
    bet: int

    def card_vals(self):
        return ["23456789TJQKA".index(x) for x in self.cards]

    def count_cards(self):
        return Counter(self.cards)

    def rank(self):
        return calc_rank(self.count_cards())

    def key(self):
        return (self.rank(), *self.card_vals())

class JokerHand(Hand):
    def card_vals(self):
        return ["J23456789TQKA".index(x) for x in self.cards]
    
    def count_cards(self):
        counts = Counter(self.cards)
        if len(counts) == 1:
            # already 5 of a kind
            return counts
        if 'J' not in counts:
            # no wild cards
            return counts
        wild = counts.pop("J")
        most_common_card, _ = counts.most_common(1)[0]
        counts[most_common_card] += wild
        return counts
    
    @staticmethod
    def from_hand(hand: Hand):
        return JokerHand(hand.cards, hand.bet)


def calc_rank(counts: Counter):
    if any(x==5 for x in counts.values()):
        return 7
    if any(x==4 for x in counts.values()):
        return 6
    if any(x==3 for x in counts.values()) and any(x==2 for x in counts.values()):
        return 5
    if any(x==3 for x in counts.values()):
        return 4
    if sum(x==2 for x in counts.values())==2:
        return 3
    if any(x==2 for x in counts.values()):
        return 2
    return 1

def get_input(path) -> List[Hand]:
    hands = []
    with open(path) as f:
        for line in f:
            cards, bet = line.strip().split(" ")
            hands.append(Hand(cards, int(bet)))
    return hands

def part1():
    hands = get_input("2023-Day07.txt")
    hands.sort(key=lambda x: x.key())
    total = sum((i+1)*x.bet for i, x in enumerate(hands))
    return total

def part2():
    hands = get_input("2023-Day07.txt")
    hands = [JokerHand.from_hand(x) for x in hands]
    hands.sort(key=lambda x: x.key())
    total = sum((i+1)*x.bet for i, x in enumerate(hands))
    return total


# 250370104
print("part1: ", part1())

# 251735672
print("part2: ", part2())