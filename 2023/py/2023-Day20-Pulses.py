from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Dict, List, Set, Tuple, Union


class Pulse(Enum):
    LOW = 1
    HIGH = 2

@dataclass(frozen=True)
class Message:
    node_to: str
    signal: Pulse
    node_from: str

    def __repr__(self):
        return f"{self.node_from} -{self.signal}> {self.node_to}"

@dataclass
class Node:
    name: str
    outputs_to: List[str]

    def process(self, signal: Pulse, from_node: str):
        raise NotImplementedError()

    def send(self, signal: Pulse):
        return [Message(node, signal, self.name) for node in self.outputs_to]
    
    def link(self, other: str):
        pass
    
    def state(self):
        return ""
    
    @staticmethod
    def parse(line: str):
        name, nodes_raw = re.split(" -> ", line)
        nodes = nodes_raw.split(", ")
        if name == "broadcaster":
            return BroadcastNode(name, nodes)
        if name.startswith("%"):
            return FlipFlopNode(name.lstrip("%"), nodes)
        if name.startswith("&"):
            return ConjunctionNode(name.lstrip("&"), nodes)
        if name == "output":
            return OutputNode(name, [])
        raise Exception("Unable to identiy node type: " + line)

@dataclass
class BroadcastNode(Node):
    inputs: Dict[str, bool] = field(default_factory=dict)

    def process(self, signal: Pulse, from_node: str):
        return self.send(signal)
    
    def link(self, other: str):
        self.inputs[other] = True

@dataclass
class OutputNode(Node):
    last_signal: Union[Pulse, None] = None
    inputs: Dict[str, bool] = field(default_factory=dict)

    def process(self, signal: Pulse, from_node: str):
        self.last_signal = signal
        return []
    
    def link(self, other: str):
        self.inputs[other] = True

@dataclass
class FlipFlopNode(Node):
    is_on: bool = False
    inputs: Dict[str, bool] = field(default_factory=dict)

    def process(self, signal: Pulse, from_node: str):
        if signal == Pulse.HIGH:
            return # do nothing
        self.is_on = not self.is_on
        return self.send(Pulse.HIGH if self.is_on else Pulse.LOW)
    
    def link(self, other: str):
        self.inputs[other] = True
    
    def state(self):
        return "1" if self.is_on else "0"

@dataclass
class ConjunctionNode(Node):
    inputs: Dict[str, Pulse] = field(default_factory=dict)

    def process(self, signal: Pulse, from_node: str):
        self.inputs[from_node] = signal
        send_pulse = Pulse.HIGH
        if all(v == Pulse.HIGH for v in self.inputs.values()):
            send_pulse = Pulse.LOW
        return self.send(send_pulse)
    
    def link(self, other: str):
        self.inputs[other] = Pulse.LOW

    def state(self):
        return "".join("H" if v==Pulse.HIGH else "L" for v in self.inputs.values())

def get_input(path):
    nodes: Dict[str, Node] = {}
    with open(path) as f:
        for line in f:
            node = Node.parse(line.strip())
            nodes[node.name] = node
    # link up inputs for Conjunction nodes
    empty_outs = []
    for node in nodes.values():
        for connection in node.outputs_to:
            if connection not in nodes:
                new_node = OutputNode(connection, [])
                new_node.link(node.name)
                empty_outs.append(new_node)
            else:
                nodes[connection].link(node.name)
    for node in empty_outs:
        nodes[node.name] = node
    return nodes


def process_messages(nodes: Dict[str, Node]):    
    low_count = 0
    high_count = 0
    init_message = Message("broadcaster", Pulse.LOW, "button")
    queue = deque([init_message])
    while queue:
        message = queue.popleft()
        if message.signal == Pulse.HIGH:
            high_count += 1
        else:
            low_count += 1
        result = nodes[message.node_to].process(message.signal, message.node_from)
        if result:
            queue.extend(result)
    return (low_count, high_count)

# StateCache = Dict[str, Tuple[str, Tuple[int, int]]]

# def calc_state(nodes: Dict[str, Node]):
#     return "".join(v.state() for v in nodes.values())

# def find_cycle(nodes: Dict[str, Node]):
#     state_cache: StateCache = {}
#     key_start = calc_state(nodes)
#     key_out = key_start
#     while key_out not in state_cache:
#         key_in = key_out
#         result = process_messages(nodes)
#         key_out = calc_state(nodes)
#         state_cache[key_in] = (key_out, result)
#     return key_start, state_cache

# def result_generator(nodes: Dict[str, Node]):
#     key, state_cache  = find_cycle(nodes)
#     while True:
#         key, value = state_cache[key]
#         yield value

def part1():
    input = get_input("2023/py/2023-Day20.txt")
    low, high = 0, 0
    for _ in range(1000):
        press_low, press_high = process_messages(input)
        low += press_low
        high += press_high
    return low * high

def part2():
    input = get_input("2023/py/2023-Day20.txt")
    presses = 0
    while input["rx"].last_signal != Pulse.LOW:
        process_messages(input)
        presses += 1
    return presses


# 737679780
print("part1: ", part1())

#print("part2: ", part2())