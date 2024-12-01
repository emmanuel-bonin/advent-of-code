import heapq
from numpy import Inf

class Tile:
  def __init__(self, row, col, type):
    self.row = row
    self.col = col
    self.type = type

  def __repr__(self):
    return self.type

  def __hash__(self):
    return self.row * 10 + self.col

class Map:
  def __init__(self, nb_rows, nb_cols):
    self.graph = {}
    self.nodes = []
    self.nb_rows = nb_rows
    self.nb_cols = nb_cols
    self.tiles = [[]] * nb_rows
    for i in range(nb_rows):
      self.tiles[i] = [None] * nb_cols

  def __repr__(self):
    s = ''
    for row in range(self.nb_rows):
      for col in range(self.nb_cols):
        s += self.tiles[row][col].__str__()
      s += '\n'
    return s

  def init_graph(self):
    nodes = self.nodes.copy()
    while len(nodes):
      node = nodes.pop(0)
      self.graph[hash(node)] = []
      for n in nodes:
        if n.row == node.row and n.col == node.col - 1:
          if n.type == '<':
            nn = next((x for x in nodes if x.row == n.row and x.col == node.col - 2), None)
            self.graph[hash(node)].append((hash(nn), 2))
          else:
            self.graph[hash(node)].append((hash(n), 1))
        elif n.row == node.row and n.col == node.col + 1:
          if n.type == '>':
            nn = next((x for x in nodes if x.row == n.row and x.col == node.col + 2), None)
            self.graph[hash(node)].append((hash(nn), 2))
          else:
            self.graph[hash(node)].append((hash(n), 1))
        elif n.col == node.col and n.row == node.row - 1:
          if n.type == '^':
            nn = next((x for x in nodes if x.col == node.col and x.row == node.row - 2), None)
            self.graph[hash(node)].append((hash(nn), 2))
          else:
            self.graph[hash(node)].append((hash(n), 1))
        elif n.col == node.col and n.row == node.row + 1:
          if n.type == 'v':
            nn = next((x for x in nodes if x.col == node.col and x.row == node.row + 2), None)
            self.graph[hash(node)].append((hash(nn), 2))
          else:
            self.graph[hash(node)].append((hash(n), 1))

def lazy_dijkstras(graph, root):
  n = len(graph)
  # set up "inf" distances
  dist = [Inf for _ in range(n)]
  # set up root distance
  dist[root] = 0
  # set up visited node list
  visited = [False for _ in range(n)]
  # set up priority queue
  pq = [(0, root)]
  # while there are nodes to process
  while len(pq) > 0:
    # get the root, discard current distance
    _, u = heapq.heappop(pq)
    # if the node is visited, skip
    if visited[u]:
      continue
    # set the node to visited
    visited[u] = True
    # check the distance and node and distance
    for v, l in graph[u]:
      # if the current node's distance + distance to the node we're visiting
      # is less than the distance of the node we're visiting on file
      # replace that distance and push the node we're visiting into the priority queue
      if dist[u] + l < dist[v]:
        dist[v] = dist[u] + l
        heapq.heappush(pq, (dist[v], v))
  return dist

def main():
  # f = open('./input.txt', 'r')
  f = open('./example.txt', 'r')

  lines = f.readlines()
  grid = Map(len(lines), len(lines[0].replace('\n', '').strip()))
  start_tile = None
  for row in range(len(lines)):
    l = lines[row]
    l = l.replace('\n', '').strip()
    for col in range(len(l)):
      tile = Tile(row, col, l[col])
      if row == 0 and col == 1:
        start_tile = tile
      grid.tiles[row][col] = tile
      if l[col] != '#':
        grid.nodes.append(tile)
  grid.init_graph()
  res = lazy_dijkstras(grid.graph, hash(start_tile))
  print(res)

if __name__ == "__main__":
  main()
