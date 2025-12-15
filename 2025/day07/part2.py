from functools import lru_cache

f = open('input.txt', 'r')
lines = [line.strip() for line in f.readlines()]
f.close()

class Node:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.connected = []
        self.cpt = 0
    def __repr__(self):
        res = f'({self.x}, {self.y}) => ['
        for node in self.connected:
            if node is not None:
                res += f'({node.x}, {node.y}),'
        return res+']'

res = 0
start_node = None
nodes_by_y = {}

for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == 'S':
            start_node = Node(x, y)
            continue
        if lines[y][x] == '^':
            if nodes_by_y.get(y) is None:
                nodes_by_y[y] = []
            nodes_by_y[y].append(Node(x, y))

def get_next_node(x, start_y):
    for _, y in enumerate(nodes_by_y.keys()):
        if y <= start_y:
            continue
        for n in nodes_by_y[y]:
            if x == n.x:
                return n
    return None

start_node.connected.append(get_next_node(start_node.x, start_node.y))

@lru_cache(maxsize=None)
def count_timelines(node):
    res = 0
    if len(node.connected) == 0:
        return 1
    for n in node.connected:
        res += count_timelines(n)
    return res+1

for i, k in enumerate(nodes_by_y.keys()):
    for n in nodes_by_y[k]:
        n1 = get_next_node(n.x-1, n.y)
        n2 = get_next_node(n.x+1, n.y)
        if n1 is not None:
            n.connected.append(n1)
        if n2 is not None:
            n.connected.append(n2)

print(count_timelines(start_node))
