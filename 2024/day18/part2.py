import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# config = {
#   'file': 'example.txt',
#   'width': 7,
#   'height': 7,
#   'n_bytes': 12
# }
config = {
    'file': 'input.txt',
    'width': 71,
    'height': 71,
    'n_bytes': 1024
}

f = open(config['file'], 'r')
lines = f.readlines()
f.close()

matrix = []
for y in range(config['height']):
    matrix.append([])
    for x in range(config['width']):
        matrix[y].append(1)

for i in range(len(lines)):
    if i >= config['n_bytes']:
        break
    x, y = lines[i].strip('\n').split(',')
    x = int(x)
    y = int(y)
    matrix[y][x] = 0


def print_map(matrix, path=None):
    s = ''
    for a in range(len(matrix)):
        for b in range(len(matrix[a])):
            if path is not None:
                found = False
                for p in range(len(path)):
                    x, y = path[p]
                    if a == y and b == x:
                        s += 'O'
                        found = True
                        break
                if not found:
                    s += '#' if matrix[a][b] == 0 else '.'
            else:
                s += '#' if matrix[a][b] == 0 else '.'
        s += '\n'
    print(s)


finished = False
while not finished:
    x, y = lines[config['n_bytes'] - 1].strip('\n').split(',')
    x = int(x)
    y = int(y)
    config['n_bytes'] += 1
    matrix[y][x] = 0
    matrix_arr = np.array(matrix)
    grid = Grid(matrix=matrix_arr)
    start = grid.node(0, 0)
    end = grid.node(config['width'] - 1, config['height'] - 1)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)
    if len(path) == 0:
        print('no path found with byte', (x, y))
        finished = True
    else:
        print('found a path when adding byte', (x, y))
