from functools import lru_cache

class Node:
    def __init__(self, name):
        self.name = name
        self.output = []
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return f"{self.name}: {[o.name for o in self.output]}"

@lru_cache(maxsize=None)
def count_possibilities(node, fft=False, dac=False):
    res = 0
    if node.name == "fft":
        fft = True
    if node.name == "dac":
        dac = True
    for _, o in enumerate(node.output):
        if o.name == "out":
            return 1 if fft and dac else 0
        res += count_possibilities(o, fft, dac)
    return res

def main():
    raw_nodes = list()
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            arr = line.split(' ')
            raw_nodes.append(Node(arr[0][:-1]))
        # iterate in nodes and add them their outputs
        for n in raw_nodes:
            for line in lines:
                if line.startswith(n.name):
                    arr = line.split(" ")[1:]
                    for e in arr:
                        if e == "out":
                            n.output.append(Node("out"))
                        else:
                            for c in raw_nodes:
                                if c.name == e:
                                    n.output.append(c)
                                    break
    start_node = None
    for n in raw_nodes:
        if n.name == "svr":
            start_node = n
            break
    res = count_possibilities(start_node, False, False)
    print(res)

main()
