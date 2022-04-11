
from dataclasses import dataclass

@dataclass
class ImgPixels:
    px: set
    rmin: int
    rmax: int
    cmin: int
    cmax: int
    fill: int

def lightpix(image) -> ImgPixels:
    pixels = set()
    R = len(image)
    C = len(image[0])
    minr, maxr = float('inf'), float('-inf')
    minc, maxc = minr, maxr
    for r in range(R):
        for c in range(C):
            if image[r][c] == 1:
                minr, maxr = min(minr, r), max(maxr, r)
                minc, maxc = min(minc, c), max(maxc, c)
                pixels.add((r,c))
    return ImgPixels(pixels, minr, maxr, minc, maxc, 0)

def get_input(filename):
    image = []
    with open(filename) as f:
        it = iter(x.strip() for x in f)
        algorithm = [int(x=="#") for x in next(it)]
        next(it)
        while (line:=next(it, None)) is not None:
            image.append([int(x=="#") for x in line])
    return algorithm, lightpix(image)
    
def display(pixels:ImgPixels):
    R = pixels.rmax - pixels.rmin + 1
    C = pixels.cmax - pixels.cmin + 1
    roff = pixels.rmin
    coff = pixels.rmin
    image = [["."] * C for _ in range(R)]
    for r, c in pixels.px:
        image[r-roff][c-coff] = "#"
    for row in image:
        print("".join(row))


dirs = ((-1, -1), (-1, 0), (-1, 1), 
        (0, -1), (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1))

def enhance(algo, pixels: ImgPixels):
    result = set()
    minr, maxr = float('inf'), float('-inf')
    minc, maxc = minr, maxr
    for r in range(pixels.rmin-1, pixels.rmax+2):
        for c in range(pixels.cmin-1, pixels.cmax+2):
            idx = 0
            for dr, dc in dirs:
                in_reg = pixels.rmin <= r+dr <= pixels.rmax and \
                    pixels.cmin <= c+dc <= pixels.cmax
                if (r+dr, c+dc) in pixels.px or (pixels.fill==1 and not in_reg):
                    idx = idx*2 + 1
                else:
                    idx = idx*2
            if algo[idx] == 1:
                minr, maxr = min(minr, r), max(maxr, r)
                minc, maxc = min(minc, c), max(maxc, c)
                result.add((r, c))
    if pixels.fill == 0:
        fill = algo[0]
    else:
        fill = algo[-1]
    return ImgPixels(result, minr, maxr, minc, maxc, fill)

algorithm, image = get_input("2021-Day20.txt")
for _ in range(50):
    image = enhance(algorithm, image)
print(len(image.px))

