
from bisect import bisect_right
from dataclasses import dataclass
from typing import List

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

@dataclass
class Run:
    start: int
    length: int

    def end(self):
        return self.start + self.length - 1
    
    @staticmethod
    def from_start_end(start, end):
        return Run(start, end-start+1)

@dataclass
class MapDef:
    dest_start: int
    source_start: int
    length: int

    def source_has_overlap(self, run: Run):
        return run.start <= self.source_end() and run.end() >= self.source_start
    
    def source_end(self):
        return self.source_start + self.length - 1
    
    def source_split(self, run: Run):
        assert(self.source_has_overlap(run))
        if run.start < self.source_start:
            # starts before
            left = Run.from_start_end(run.start, self.source_start-1)
        else:
            left = None
        overlap = Run.from_start_end(max(self.source_start, run.start), min(self.source_end(), run.end()))
        if run.end() > self.source_end():
            #ends after
            right = Run.from_start_end(self.source_end() + 1, run.end())
        else:
            right = None
        return left, overlap, right
    
    def transform(self, run: Run):
        return Run(run.start + (self.dest_start - self.source_start), run.length)

@dataclass
class MapTable:
    input: str
    output: str
    maps: List[MapDef]

def find_le(a, x):
    'Find rightmost index less than or equal to x'
    return bisect_right(a, x) - 1

def get_input(path):
    def get_seeds(line: str):
        line = line.removeprefix("seeds: ")
        return [int(x) for x in line.split(" ")]
    
    def parse_table_start(line: str):
        line = line.removesuffix(" map:")
        parts = line.split("-")
        return MapTable(parts[0], parts[2], [])
    
    def parse_table_row(line: str):
        parts = [int(x) for x in line.split(" ")]
        return MapDef(*parts)
    
    with open(path) as f:
        lines = (x.strip() for x in f)
        seeds = get_seeds(next(lines))
        assert("" == next(lines))
        mappings = []
        while True:
            try:
                line = next(lines)
                mapping =  parse_table_start(line)
                mappings.append(mapping)
                line = next(lines)
                while line != "":
                    mapping.maps.append(parse_table_row(line))
                    line = next(lines)
            except StopIteration:
                break
        return seeds, mappings
    
def create_transform(table: MapTable):
    parts = sorted(table.maps, key=lambda x: x.source_start)
    keys = [x.source_start for x in parts]
    def transform(x):
        i = find_le(keys, x)
        if i >= 0:
            range = parts[i]
            if range.source_start <= x <= range.source_start + range.length:
                return x-range.source_start + range.dest_start
        return x
    return transform

def create_transfomer(tables: List[MapTable]):
    txs = [create_transform(x) for x in tables]
    def transform(x):
        for tx in txs:
            x = tx(x)
        return x
    return transform

def create_range_transform(table: MapTable):
    parts = sorted(table.maps, key=lambda x: x.source_start)
    def transform(runs: List[Run]) -> List[Run]:
        result: List[Run] = []
        run_idx = 0
        part_idx = 0
        current_run = runs[run_idx]
        while True:
            next_run = False
            while part_idx < len(parts) and not parts[part_idx].source_has_overlap(current_run):
                part_idx += 1
            if part_idx < len(parts):
                left, overlap, right = parts[part_idx].source_split(current_run)
                if left:
                    result.append(left)
                if overlap:
                    result.append(parts[part_idx].transform(overlap))
                if right:
                    current_run = right
                else:
                    next_run = True
            else:
                result.append(current_run)
                next_run = True
            if next_run:
                run_idx += 1
                if run_idx >= len(runs):
                    break
                current_run = runs[run_idx]
        result.sort(key = lambda x: x.start)
        return result
        
    return transform

def create_range_transfomer(tables: List[MapTable]):
    txs = [create_range_transform(x) for x in tables]
    def transform(x: List[Run]) -> List[Run]:
        for tx in txs:
            x = tx(x)
        return x
    return transform
    
def part1():
    seeds, mappings = get_input("2023-Day05.txt")
    tx = create_transfomer(mappings)
    return min([tx(x) for x in seeds])

def part2():
    seeds, mappings = get_input("2023-Day05.txt")
    tx = create_range_transfomer(mappings)
    seed_runs = [Run(*x) for x in pairwise(seeds)]
    bests = [tx([x])[0].start for x in seed_runs]
    return min(bests)

# 174137457
print("part1:", part1())

# 1493866
print("part2:", part2())