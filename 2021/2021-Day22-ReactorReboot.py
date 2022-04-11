import re
from dataclasses import dataclass
from itertools import product
from collections import defaultdict
from bisect import bisect_left, bisect_right

@dataclass
class Region:
    value: bool
    x: tuple[int]
    y: tuple[int]
    z: tuple[int]

commands: list[Region] = []
with open("2021-Day22-Test2.txt") as f:
    for line in (x.strip() for x in f):
        if line.startswith("#"): continue
        parts = re.split(r'(?:[ =,]|\.\.)', line)
        commands.append(Region(parts[0]=='on', (int(parts[2]), int(parts[3])),
        (int(parts[5]), int(parts[6])), (int(parts[8]), int(parts[9]))))

def naive_one(commands, gmin, gmax):
    R = gmax-gmin+1
    cube =[
        [[False] * R for _ in range(R)] for _ in range(R)
    ]

    def limited_range(rmin, rmax):
        def gen (a, b):
            a = max(a, rmin)
            b = min(b, rmax)
            if a>b:
                return range(0)
            else:
                return range(a, b+1)
        return gen

    total = 0
    lrange = limited_range(gmin, gmax)
    for idx, cmd in enumerate(commands):
        print(idx, cmd)
        for x in lrange(*cmd.x):
            for y in lrange(*cmd.y):
                for z in lrange(*cmd.z):
                    if cmd.value != cube[x-gmin][y-gmin][z-gmin]:
                        cube[x-gmin][y-gmin][z-gmin]= cmd.value
                        if cmd.value:
                            total += 1
                        else:
                            total -= 1
        print(total)
    return(total)

print(naive_one(commands, -50, 50))

def rpoints(r:Region):
    for x in range(r.x[0], r.x[1]+1):
        for y in range(r.y[0], r.y[1]+1):
            for z in range(r.z[0], r.z[1]+1):
                print (x, y, z)

def overlaps(x1:int, x2:int, y1:int, y2:int) -> bool:
    return y1 <= x2 and y2 >= x1

def overlap3d(r1:Region, r2:Region) -> bool:
    return overlaps(*r1.x, *r2.x) and \
        overlaps(*r1.y, *r2.y) and \
        overlaps(*r1.z, *r2.z)

def envelops(x1:int, x2:int, y1:int, y2:int) -> bool:
    return y1 <= x1 and y2 >= x2

def envelop3d(r1:Region, r2:Region) -> bool:
    return envelops(*r1.x, *r2.x) and \
        envelops(*r1.y, *r2.y) and \
        envelops(*r1.z, *r2.z)

def porder(start1, end1, start2, end2):
    parts = []
    pos = 0
    if start1 < start2:
        parts.append(((start1, start2-1), 1))
        pos = start2
    elif start2 < start1:
        parts.append(((start2, start1-1), 2))
        pos = start1
    else:
        pos = start1
    if end1 < end2:
        parts.append(((pos, end1), 3))
        pos = end1 + 1
    elif end2 < end1:
        parts.append(((pos, end2), 3))
        pos = end2 + 1
    else:
        parts.append(((pos, end1), 3))
        return parts
    if end2 >= pos:
        parts.append(((pos, end2), 2))
    else:
        parts.append(((pos, end1), 1))
    return parts

def expand(r1:Region, r2:Region):
    sx = porder(*r1.x, *r2.x)
    sy = porder(*r1.y, *r2.y)
    sz = porder(*r1.z, *r2.z)

    regions = []
    for x,y,z in product(sx, sy, sz):
        isin1 = x[1]&1 and y[1]&1 and z[1]&1
        isin2 = x[1]&2 and y[1]&2 and z[1]&2
        if (isin2 and r2.value) or (not isin2 and isin1):
            newr = Region(True, x[0], y[0], z[0])
            regions.append(newr)
    return regions

def oncount(r:Region):
    return (r.x[1]-r.x[0]+1) * (r.y[1] - r.y[0]+1) * (r.z[1] - r.z[0] + 1)

def transform_region(cmd, regions):
    overlapped = False
    i = 0
    while i < len(regions):
        if overlap3d(regions[i], cmd):
            overlapped = True
            if envelop3d(regions[i], cmd):
                if cmd.value:
                    regions[i] = cmd
                    i += 1
                else:
                    del regions[i]
            else:
                newregions = expand(regions[i], cmd)
                del regions[i]
                for nr in newregions:
                    regions.insert(i, nr)
                i += len(newregions)
        else:
            i += 1
    if not overlapped and cmd.value:
        regions.append(cmd)

def rangewalk(min, max, size=10):
    a = divmod(min, size)
    b = divmod(max, size)
    if a[0] == b[0]:
        yield (min, max), a[0], False
        return
    if a[1] > 1:
        yield (min, (a[0]+1)*size-1), a[0], False
        i = a[0] + 1
    else:
        i = a[0]
    while i < b[0]:
        yield (i*size, (i+1)*size-1), i, True
        i+= 1
    yield (b[0]*size, max), b[0], b[1]==size-1

def regionwalk(r:Region, size=10) -> tuple[Region, tuple[int], bool]:
    for sx, gx, fx in rangewalk(*r.x, size=size):
        for sy, gy, fy in rangewalk(*r.y, size=size):
            for sz, gz, fz in rangewalk(*r.z, size=size):
                yield Region(r.value, sx, sy, sz), (gx, gy, gz), (fx and fy and fz)

def totalcount(r):
    total = 0
    for x in r.values():
        total += sum([oncount(y) for y in x])
    return total



# regions = defaultdict(list)
# for idx, cmd in enumerate(commands):
#     for region, key, isfull in regionwalk(cmd, size=100):
#         if isfull:
#             if region.value:
#                 regions[key] = [region]
#             else:
#                 del regions[key]
#         else:
#             reg = regions[key]
#             transform_region(region, reg)
#             if len(reg)<1:
#                 del regions[key]
#     print(idx, cmd)
#     print(totalcount(regions))
#     print("step")


def get_global_grid(commands):
    def extendobs(uv):
        uv = sorted(uv)
        r = []
        for i in uv:
            for offset in (-1, 0, 1):
                if i + offset not in r:
                    r.append(i + offset)
        return r
        
    ux, uy, uz = set(), set(), set()
    for cmd in commands:
        ux.update(cmd.x)
        uy.update(cmd.y)
        uz.update(cmd.z)
    ux = extendobs(ux)
    uy = extendobs(uy)
    uz = extendobs(uz)
    return ux, uy, ux

def global_idx_range(min, max, grid):
    return range(bisect_left(grid, min), bisect_right(grid, max))

def score(grid, gx, gy, gz):
    NX, NY, NZ = len(grid), len(grid[0]), len(grid[1])
    total = 0
    for x in range(0,NX-1):
        for y in range(0,NY-1):
            for z in range(0,NZ-1):
                if grid[x][y][z]:
                    total += (gx[x+1]-gx[x]) * (gy[y+1]-gy[y]) * (gz[z+1]-gz[z])
    return total

def process(commands):
    gx, gy, gz = get_global_grid(commands)
    grid =[
        [[False] * len(gz) for _ in range(len(gy))] for _ in range(len(gx))
    ]
    for idx, cmd in enumerate(commands):
        print(idx, cmd)
        for x in global_idx_range(*cmd.x, gx):
            for y in global_idx_range(*cmd.y, gy):
                for z in global_idx_range(*cmd.z, gz):
                    grid[x][y][z] = cmd.value
        print(score(grid, gx, gy, gz))
    
    return score(grid, gx, gy, gz)
    

print(process(commands))




