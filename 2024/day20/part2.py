import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

f = open('input.txt', 'r')
lines = f.readlines()

map = []
start_x = 0
start_y = 0
end_x = 0
end_y = 0
initial_matrix = []
for y in range(len(lines)):
    line = lines[y].strip('\n')
    map.append([])
    initial_matrix.append([])
    for x in range(len(line)):
        map[y].append(line[x])
        if line[x] == 'S':
            start_x = x
            start_y = y
        elif line[x] == 'E':
            end_x = x
            end_y = y
        initial_matrix[y].append(1 if line[x] == '.' or line[x] == 'S' or line[x] == 'E' else 0)
f.close()

raw_matrices = []
finished = False
cache = {}
print('Generating matrices...')
while not finished:
    finished = True
    cheated = False
    matrix = []
    for y in range(len(map)):
        matrix.append([])
        for x in range(len(map[y])):
            if map[y][x] == '#':
                if (not cheated and (y > 0 and y < len(map) - 1 and x > 0 and x < len(map[y]) - 1) and str(
                        x) + '_' + str(y) not in cache):
                    cache[str(x) + '_' + str(y)] = True
                    matrix[y].append(1)
                    finished = False
                    cheated = True
                else:
                    matrix[y].append(0)
            else:
                matrix[y].append(1)
    raw_matrices.append(matrix)
    print('Generated', len(raw_matrices), 'matrices')


def run_matrix(matrix, start_x, start_y, end_x, end_y):
    grid = Grid(matrix=matrix)
    start = grid.node(start_x, start_y)
    end = grid.node(end_x, end_y)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    return len(path)


initial_res = run_matrix(initial_matrix, start_x, start_y, end_x, end_y)


def resolve(_id, raw_matrices, initial_res, start_x, start_y, end_x, end_y):
    n = 0
    result = {}
    i = 0
    for m in raw_matrices:
        res = run_matrix(m, start_x, start_y, end_x, end_y)
        saved = initial_res - res
        if saved >= 100:
            n += 1
        print('[' + _id + '] Matrix', i, '/', len(raw_matrices), '(',
              str(round((i / len(raw_matrices)) * 100, 3)) + '%)', 'saved', saved, 'steps')
        i += 1
    print('[' + _id + '] Result:', n)


resolve(raw_matrices, initial_res, start_x, start_y, end_x, end_y)
