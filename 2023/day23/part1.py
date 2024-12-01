import heapq
from numpy import Inf

class Tile:
  def __init__(self, row, col, type):
    self.row = row
    self.col = col
    self.type = type
    self.weight = 0
    self.visited = False

  def __repr__(self):
    return self.type
    # return f'[{self.row} {self.col} {self.weight}] ({self.type})'

  def __hash__(self):
    return self.row * 10 + self.col

  def __eq__(self, other):
    return self.row == other.row and self.col == other.col

class Map:
  def __init__(self, nb_rows, nb_cols):
    self.nb_rows = nb_rows
    self.nb_cols = nb_cols
    self.tiles = [[]] * nb_rows
    self.path_tiles = []
    for i in range(nb_rows):
      self.tiles[i] = [None] * nb_cols

  def __repr__(self):
    s = ''
    for row in range(self.nb_rows):
      for col in range(self.nb_cols):
        s += self.tiles[row][col].__str__()
      s += '\n'
    return s

def print_grid(grid):
  s = ''
  for row in range(grid.nb_rows):
    for col in range(grid.nb_cols):
      if grid.tiles[row][col].visited == True:
        s += 'O'
      else:
        s += grid.tiles[row][col].__str__()
    s += '\n'
  print(s)

def main():
  # f = open('./input.txt', 'r')
  f = open('./example.txt', 'r')

  lines = f.readlines()
  grid = Map(len(lines), len(lines[0].replace('\n', '').strip()))
  for row in range(len(lines)):
    l = lines[row]
    l = l.replace('\n', '').strip()
    for col in range(len(l)):
      tile = Tile(row, col, l[col])
      grid.tiles[row][col] = tile
      if tile.type != '#':
        grid.path_tiles.append(tile)
  current = grid.path_tiles[0]
  end = grid.path_tiles[-1]
  # Currently, the algorithm finds multiple path to end,
  # but either stop to first found, or infinite loop.
  # TODO: to avoid this, iterate on tiles while there is only one path
  # if a tile has multiple children, store this tile in a list
  # once a path has been found from this tile, store the result, remove the tile from start points
  # and move on to the next starting point
  # current = grid.path_tiles[0]
  # end = grid.path_tiles[-1]
  # current.visited = True
  # results = []
  # next = [x for x in grid.path_tiles if (x.visited == False or x.weight != current.weight + 1) and ((x.row == current.row and (x.col == current.col - 1 or x.col == current.col + 1)) or (x.col == current.col and (x.row == current.row - 1 or x.row == current.row + 1)))]
  # for a in next:
  #   a.weight = current.weight + 1
  # finished = False
  # while finished == False:
  #   finished = True
  #   for i in range(len(next)):
  #     n = next.pop(i)
  #     current = n
  #     current.visited = True
  #     print_grid(grid)
  #     n.visited = True
  #     if current == end:
  #       results.append(current.weight)
  #     else:
  #       new_next = [x for x in grid.path_tiles if (x.visited == False or x.weight != current.weight + 1) and ((x.row == current.row and (x.col == current.col - 1 or x.col == current.col + 1)) or (x.col == current.col and (x.row == current.row - 1 or x.row == current.row + 1)))]
  #       for a in new_next:
  #         a.weight = current.weight + 1
  #       next += new_next
  #       finished = False
  #       break
  # print(results)

if __name__ == "__main__":
  main()
