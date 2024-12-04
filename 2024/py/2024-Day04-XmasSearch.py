
def read_grid(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]
    
g = read_grid('2024-Day04.txt')

def search(g, r=0, c=0, target="XMAS", dr=1, dc=1):
    if r<0 or r>=len(g) or c<0 or c>=len(g[0]):
        return 0
    if g[r][c] == target[0]:
        if len(target)==1:
            return 1
        else:
            return search(g, r+dr, c+dc, target[1:], dr, dc)
    return 0

def search_all(g, target="XMAS"):
    total = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr!=0 or dc!=0:
                        if search(g, i, j, target, dr, dc):
                            total += 1
    return total

def check_diag(g, r, c):
    return ((g[r+1][c+1]=="M" and g[r-1][c-1]=="S") or \
        (g[r+1][c+1]=="S" and g[r-1][c-1]=="M")) and \
        ((g[r-1][c+1]=="M" and g[r+1][c-1]=="S") or \
        (g[r-1][c+1]=="S" and g[r+1][c-1]=="M"))
        

def search_x(g):
    total = 0
    for i in range(1, len(g)-1):
        for j in range(1, len(g[0])-1):
            if g[i][j] != "A":
                continue
            if check_diag(g, i, j):
                total +=1
    return total

print("Part 1:", search_all(g))
# 2370

print("Part 2:", search_x(g))
# 1908