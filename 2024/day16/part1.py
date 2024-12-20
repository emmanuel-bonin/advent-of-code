import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

f = open('input.txt', 'r')
lines = f.readlines()

map = []
raw_matrix = []
start_x = 0
start_y = 0
end_x = 0
end_y = 0
for y in range(len(lines)):
  raw_matrix.append([])
  map.append([])
  for x in range(len(lines[y])):
    if lines[y][x] == 'S':
      raw_matrix[y].append(1)
      map[y].append('S')
      start_x = x
      start_y = y
    elif lines[y][x] == 'E':
      raw_matrix[y].append(1)
      map[y].append('E')
      end_x = x
      end_y = y
    elif lines[y][x] == '.':
      if ((lines[y-1][x] == '.' and lines[y-2][x] != '.') or
         (lines[y+1][x] == '.' and lines[y+2][x] != '.') or
         (lines[y][x-1] == '.' and lines[y][x-2] != '.') or
         (lines[y][x+1] == '.' and lines[y][x+2] != '.')):
        raw_matrix[y].append(1000)
      else:
        raw_matrix[y].append(1)
      map[y].append('.')
    elif lines[y][x] == '#':
      map[y].append('#')
      raw_matrix[y].append(0)

f.close()

# for i in range(len(raw_matrix)):
#   for j in range(len(raw_matrix[i])):
#     print('\t' + str(raw_matrix[i][j]), end='')
#   print()

def debug_map(map, path):
  s = ''
  for a in range(len(map)):
    for b in range(len(map[a])):
      found = False
      for p in range(len(path)):
        x, y = path[p]
        if a == y and b == x:
          s += '^'
          found = True
          break
      if not found:
        s += map[a][b]
    s += '\n'
  print(s)
grid = Grid(matrix=np.array(raw_matrix))

start = grid.node(start_x, start_y)
end = grid.node(end_x, end_y)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)

n_turn = 0
n_forward = 0
prev_dir = 'R'
old_x = 0
old_y = 0
diff_x = 0
diff_y = 0
result = 0
for i in range(len(path)):
  x, y = path[i]
  if i != 0:
    diff_x = x - old_x
    diff_y = y - old_y
    cur_dir = None
    if diff_x == 1:
      cur_dir = 'R'
    elif diff_x == -1:
      cur_dir = 'L'
    elif diff_y == 1:
      cur_dir = 'D'
    elif diff_y == -1:
      cur_dir = 'U'

    result += 1
    n_forward += 1
    if prev_dir != cur_dir:
      result += 1000
      n_turn += 1
    prev_dir = cur_dir
  old_x = x
  old_y = y

# debug_map(map, path)
print('=>', n_turn, n_forward, n_turn * 1000 + n_forward, result)
