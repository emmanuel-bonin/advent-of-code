class Node:
  def __init__(self, name, parent=[]):
    self.name = name
    self.parent = parent
    self.children_raw = []
    self.children = []

  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return f'({self.name}: children({len(self.children)})={list(map(lambda x: x.name, self.children))}, parent={list(map(lambda x: x.name, self.parent))})'

def parse_lines(lines):
  nodes = []
  for l in lines:
    l = l.replace('\n', '').strip()
    arr = l.split(':')
    connected = arr[1].strip().split(' ')
    n = Node(arr[0])
    n.children_raw = connected
    nodes.append(n)
  for n in nodes:
    for c in n.children_raw:
      cn = Node(c)
      try:
        idx = nodes.index(cn)
      except:
        idx = -1
      if idx != -1:
        print('[current:', n.name, '] found other node named', c, 'adding parent', n.name, 'to', nodes[idx].name, 'and child', nodes[idx].name, 'to', n.name)
        nodes[idx].parent.append(n)
        n.children.append(nodes[idx])
      else:
        print('[current:', n.name, '] other node not found', c, 'adding parent', n.name, 'to', cn.name, 'and child', cn.name, 'to', n.name)
        cn.parent.append(n)
        n.children.append(cn)
  return nodes

def main():
  # f = open('./input.txt', 'r')
  f = open('./example.txt', 'r')
  lines = f.readlines()
  nodes = parse_lines(lines)
  # print(nodes)

if __name__ == "__main__":
  main()
