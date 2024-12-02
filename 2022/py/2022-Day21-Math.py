ops = {
    "+": lambda x,y: x+y, 
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x//y
}
# z = x (op) y 
# find y
right_inv = {
    "+": lambda z,x: z-x, 
    "-": lambda z,x: x-z,
    "*": lambda z,x: z//x,
    "/": lambda z,x: x//z
}
# z = x (op) y 
# find x
left_inv = {
    "+": lambda z,y: z-y, 
    "-": lambda z,y: z+y,
    "*": lambda z,y: z//y,
    "/": lambda z,y: y*z
}

class Node:
    def eval(self):
        raise NotImplementedError()

    def link(self, nodes: dict[str, 'Node']):
        raise NotImplementedError()


class LeafNode(Node):
    def __init__(self, name, val):
        self.name = name
        self.val = val
         
    def eval(self):
        return self.val

    def link(self, nodes: dict[str, 'Node']):
        pass

class OpNode(Node):
    def __init__(self, name, op, leftname, rightname):
        self.name = name
        self.op = op
        
        self.leftname = leftname
        self.rightname = rightname
        self.left = None
        self.right = None
    
    def eval(self):
        return ops[self.op](self.left.eval(), self.right.eval())

    def link(self, nodes: dict[str, 'Node']):
        self.left = nodes[self.leftname]
        self.right = nodes[self.rightname]

    def collapse(self):
        return self


def get_input(filename):
    nodes: dict[str, 'Node'] = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ")
            name = parts[0].removesuffix(":")
            if len(parts) == 4:
                nodes[name] = OpNode(name, parts[2], parts[1], parts[3])
            elif len(parts) == 2:
                nodes[name] = LeafNode(name, int(parts[1]))
    for node in nodes.values():
        node.link(nodes)
    return nodes

def part1():
    nodes = get_input("2022-Day21.txt")
    return nodes['root'].eval()

def part2():
    nodes = get_input("2022-Day21.txt")
    root = nodes['root']

    def find_human(node, path):
        if isinstance(node, OpNode):
            left = find_human(node.left, path + ('L',))
            right = find_human(node.right, path + ('R',))
            if left and right:
                raise Exception("Double Human Path")
            return left or right
        else:
            if node.name == "humn":
                return path
            else:
                return None

    node = root
    # eather than a == b, assume 0 = a - b for root
    node.op = "-"
    target = 0
    for dir in find_human(node, tuple()):
        # eval non-human node path and find new target each node
        if dir == 'L':
            other = node.right.eval()
            target = left_inv[node.op](target, other)
            node = node.left
        elif dir == 'R':
            other = node.left.eval()
            target = right_inv[node.op](target, other)
            node = node.right
    return target


print("Part 1:", part1())
# Part 1: 159591692827554

print("Part 2:", part2())
# Part 2: 3509819803065


