from copy import deepcopy


class Board:
    def __init__(self):
        self.nums = dict()
        self.rows = [0] * 5
        self.cols = [0] * 5

    def add_num(self, num, row, col):
        self.nums[num] = (row, col)
    
    def mark_num(self, num):
        if num in self.nums:
            row, col = self.nums[num]
            self.rows[row] += 1
            self.cols[col] += 1
            del self.nums[num]

    def is_winner(self):
        return any((x==5 for x in self.rows)) or \
            any((x==5 for x in self.cols))
    
    def __repr__(self) -> str:
        vals = [[""] * 5 for _ in range(5)]
        for n, (r, c) in self.nums.items():
            vals[r][c] = n
        return "---\n" + "\n".join([" ".join(str(z) for z in x) for x in vals]) + "\n---\n"
    
    def score(self):
        return sum(v for v in self.nums.keys())

boards :list[Board] = list()

with open("2021-Day04.txt") as f:
    lines = iter(x.strip() for x in f)
    nums = [int(x) for x in next(lines).split(",")]
    row = next(lines, None)
    while row is not None:
        board = Board()
        for i in range(5):
            row = next(lines)
            vals = row.split()
            for col, val in enumerate(vals):
                board.add_num(int(val), i, col)
        boards.append(board)
        row = next(lines, None)

def play_to_win(nums, boards):
    for num in nums:
        for b in boards:
            b.mark_num(num)
            if b.is_winner():
                return(b.score() * num)

def play_to_lose(nums, boards):
    boards = deepcopy(boards)
    
    for num in nums:
        for b in boards:
            b.mark_num(num)
        if len(boards)==1:
            if boards[0].is_winner():
                return(boards[0].score() * num)
        else:
            boards = list(filter(lambda x: not x.is_winner(), boards))
                

print(play_to_win(nums, boards))
print(play_to_lose(nums, boards))
                
