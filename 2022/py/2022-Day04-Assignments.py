with open("2022-Day04.txt", encoding="utf-8") as f:
    contained = 0
    overlapping = 0
    for line in (x.strip() for x in f if x):
        a, b, c, d = map(int, line.replace(",","-").split("-"))
        if a<=c and b>=d or c<=a and d>=b:
            contained += 1
            overlapping += 1
        elif c <= a <= d or c<= b <= d:
            overlapping += 1
    print(f"Contained {contained}")
    print(f"Overlapping {overlapping}")

        
