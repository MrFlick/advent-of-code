from heapq import heappush, heappop
from collections import Counter
from math import prod

def read_input(file_path: str) -> list[tuple[int, int, int]]:
    with open(file_path, "r") as file:
        return [tuple(map(int, line.split(","))) for line in file.readlines()]

def part1(input: list[tuple[int, int, int]], target: int) -> int:
    heap = []
    for i in range(len(input)-1):
        for j in range(i+1, len(input)):
            dist = (input[i][0] - input[j][0])**2 + (input[i][1] - input[j][1])**2 + (input[i][2] - input[j][2])**2
            heappush(heap, (dist, i, j))
    circuit = [i for i in range(len(input))]
    while len(heap) >0 and target>0:
        dist, i, j = heappop(heap)
        if circuit[i] == circuit[j]:
            pass
        else:            
            join = min(circuit[j], circuit[i])
            a = circuit[i]
            b = circuit[j]
            for k in range(len(circuit)):
                if circuit[k] == a or circuit[k] == b:
                    circuit[k] = join
        target -= 1
    most_common = Counter(circuit).most_common(3)
    best = [v for k, v in most_common]
    return prod(best)

def part2(input: list[tuple[int, int, int]]) -> int:
    heap = []
    for i in range(len(input)-1):
        for j in range(i+1, len(input)):
            dist = (input[i][0] - input[j][0])**2 + (input[i][1] - input[j][1])**2 + (input[i][2] - input[j][2])**2
            heap.append((dist, i, j))
    heap.sort()
    circuit = [i for i in range(len(input))]
    size = [1 for _ in range(len(input))]

    def find(x: int, circuit: list[int]) -> int:
        if circuit[x] == x:
            return x
        else:
             y = find(circuit[x], circuit)
             circuit[x] = y
             return y
    
    while heap:
        dist, i, j = heap.pop(0)
        a = find(i, circuit)
        b = find(j, circuit)
        if a != b:
            if size[a] < size[b]:
                size[b] += size[a]
                size[a] = 0
                circuit[a] = b
            else:
                size[a] += size[b]
                size[b] = 0
                circuit[b] = a
            if size[a] + size[b] == len(input):
                return input[i][0] * input[j][0]

def main():
    input_test = read_input("2025-Day08-test.txt")
    input_main = read_input("2025-Day08.txt")
    print("part 1 test", part1(input_test, 10))
    # 40
    print("part 1 main", part1(input_main, 1000))
    # 97384

    print("part 2 test", part2(input_test))
    # 25272
    print("part 2 main", part2(input_main))
    # 9003685096

if __name__ == "__main__":
    main()