from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    direction: str
    steps: int

def solveA(moves: list[Move], start_dial=50, max_dial=99) -> int:
    dial = start_dial
    result = 0
    for move in moves:
        if move.direction == "L":
            dial -= move.steps
        elif move.direction == "R":
            dial += move.steps
        while dial < 0:
            dial += max_dial + 1
        while dial > max_dial:
            dial -= max_dial + 1
        if dial == 0:
            result += 1
    return result

def solveB(moves: list[Move], start_dial=50, max_dial=99) -> int:
    from_dial = start_dial
    dial_range = max_dial + 1
    result = 0
    for move in moves:
        steps = move.steps
        while steps > dial_range:
            result += 1
            steps -= dial_range
        if move.direction == "L":
            to_dial = from_dial - steps
        elif move.direction == "R":
            to_dial = from_dial + steps
        if to_dial < 0:
            to_dial += dial_range
            if from_dial != 0:
                result += 1
        if to_dial > max_dial:
            to_dial -= dial_range
            if to_dial != 0:
                result += 1
        if to_dial == 0:
            result += 1
        from_dial = to_dial
    return result

def parse_moves(input_file: str) -> list[Move]:
    with open(input_file, "r") as file:
        moves = file.readlines()
    return [Move(direction=move[0], steps=int(move[1:])) for move in moves]

def main():
    test_moves = parse_moves("2025-Day01-test.txt")
    main_moves = parse_moves("2025-Day01.txt")
    print("test 1", solveA(test_moves))
    print("main 1", solveA(main_moves))
    # 1154

    print("test 2", solveB(test_moves))
    print("main 2", solveB(main_moves))
    # 6819

if __name__ == "__main__":
    main()