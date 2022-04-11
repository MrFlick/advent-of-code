import math
import itertools

target = {"x": [20, 30], "y": [-10, -5]}
target = {"x": [287, 309], "y": [-76, -48]}


class Proj:
    def __init__(self, vx, vy):
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 1
        if self.vx > 0:
            self.vx -= 1
        elif self.vx < 0:
            self.vx += 1
        return (self.x, self.y)

    def hit(self, target):
        while self.x <= target["x"][1] and self.y >= target["y"][0]:
            if target["x"][0] <= self.x <= target["x"][1] and \
                target["y"][0] <= self.y <= target["y"][1]:
                return True
            self.step()
        return False

# dy will always eventually hit 0. 
# we want a jump that will hit the bottof it the target
# as it makes the descent
maxy = abs(target["y"][0])-1
print((maxy *(maxy+1))//2)

def invtrinum(x):
    return math.sqrt(2*x + 1/4) - 1/2


searchmin = math.ceil(invtrinum(target["x"][0]))
searchmax = target["x"][0]

hits = 0
for vx in range(searchmin, searchmax):
    for vy in range(target["y"][0], -target["y"][0]):
        p = Proj(vx, vy)
        if p.hit(target):
            hits += 1
extra = (target["y"][1] - target["y"][0]+1) * (target["x"][1] - target["x"][0]+1)
hits += extra
print(hits)


