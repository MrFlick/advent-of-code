def get_input(filename):
    with open(filename, encoding="utf-8") as f:
        return list(f.read().strip())

 # bit wise
shapes = (
    # ----
    (30,),
    # -|-
    (8, 28, 8),
    # _|
    (28, 4, 4),
    # | 
    (16, 16, 16, 16),
    # []
    (24, 24)
)

def get_shape():
    while True:
        for i, shape in enumerate(shapes):
            yield i, shape

def get_jet(jets):
    while True:
        for jet in jets:
            yield jet
        yield "*"

def print_board(board, max=10):
    max = min(max, len(board))
    for row in reversed(board[-max:]):
        print("".join(["#" if row & 2**i else "." for i in reversed(range(7))]))

def can_move_left(shape, sx, board):
    LEFT = 64
    return not any(row & LEFT for row in shape) and all( row<<1 & board[sx+i] == 0 if sx+i < len(board) else True for i, row in enumerate(shape))

def can_move_right(shape, sx, board):
    RIGHT = 1
    return not any(row & RIGHT for row in shape) and all( row>>1 & board[sx+i] == 0 if sx+i < len(board) else True for i, row in enumerate(shape))


def stack():
    goal = 1000000000000
    jets = get_input("2022-Day17.txt")
    input = get_jet(jets)
    shapes = iter(get_shape())
    sc = 0
    board = []
    burn_shape, burn_height = 0, 0
    step_shape, step_height = 0, 0
    cache = {}
    more = -1
    for _ in range(max(2022, len(jets)*6)):
        #print("new shape")
        si, shape = next(shapes)
        
        sx = len(board) + 3
        settled = False
        while not settled:
            wind = next(input)
            if wind == "*":
                if len(board)> 7 and step_shape == 0:
                    key = (si, sx-len(board)) + tuple(board[-7:])
                    if key in cache:
                        if burn_shape == 0 and burn_height == 0:
                            burn_shape = cache[key][0]
                            burn_height = cache[key][1]
                            step_shape = sc - burn_shape
                            step_height = len(board) - burn_height
                            more = (goal - burn_shape) % step_shape
                            more_height = len(board)
                    else:
                        cache[key] = (sc, len(board))
                    #print(si, sc, len(board))
                    #print_board(board, 7)
                    #print("")
                wind = next(input)
            if wind == "<":
                if can_move_left(shape, sx, board):
                    shape = tuple(x << 1 for x in shape)
            elif wind == ">":
                if can_move_right(shape, sx, board):
                    shape = tuple(x >> 1 for x in shape)
            if sx >0 and all( row & board[sx+i-1] == 0 if sx+i-1 < len(board) else True for i, row in enumerate(shape)):
                sx -= 1
            else:
                sc += 1
                for i, row in enumerate(shape):
                    if sx + i >= len(board):
                        board.append(row)
                    else:
                        board[sx+i] |= row
                settled = True
                if sc==2022:
                    print("Part 1:", len(board))
                if more > 0 :
                    more -= 1
                if more == 0:
                    expected = burn_height + ((goal - burn_shape) // step_shape) * step_height + len(board) - more_height
                    print("Part 2:", expected)
                    more -= 1

stack()

# Part 1: 3144
# Part 2: 1565242165201
# 3116239311295 (too high)
# 1565242165199 (too low)
