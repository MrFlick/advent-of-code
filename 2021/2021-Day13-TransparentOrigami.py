sampleinput1 = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def printpaper(points, XX, YY):
    board = [['.'] * (XX+1) for _ in range(YY+1)]
    for x, y in points:
        board[y][x] = "#"
    for row in board:
        print("".join(row))

folds = []
points = set()
XX = 0
YY = 0
lines = iter(x.strip() for x in sampleinput1.split("\n"))

with open("2021-Day13.txt") as f:
    lines = iter(x.strip() for x in f)
    for line in lines:
        if line == "": break
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        XX = max(x, XX)
        YY = max(y, YY)
        points.add((x, y))
    for line in lines:
        line = line.replace("fold along ", "")
        axis, val = line.split("=")
        folds.append((axis, int(val)))


def fold(points, axis, val):
    global XX, YY
    nextp = set()
    if axis == 'x':
        for point in points:
            if point[0] > val:
                nv = point[0] - 2 * (point[0] - val)
            else:
                nv = point[0]
            nextp.add((nv, point[1]))
        XX = val-1
    elif axis == 'y':
        for point in points:
            if point[1] > val:
                nv = point[1] - 2 * (point[1] - val)
            elif point[1] < val:
                nv = point[1]
            nextp.add((point[0], nv))
        YY = val-1
    return nextp
    

#print(len(fold(points, folds[0][0], folds[0][1])))

for axis, val in folds:
    points = fold(points, axis, val)

printpaper(points, XX, YY)
    
