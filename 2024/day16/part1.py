import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

f = open('input.txt', 'r')
lines = f.readlines()
f.close()

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
            raw_matrix[y].append(1)
            map[y].append('.')
        elif lines[y][x] == '#':
            map[y].append('#')
            raw_matrix[y].append(0)


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


def is_turn(p1, p2, p3):
    return not ((p1.x == p2.x and p2.x == p3.x) or (p1.y == p2.y and p2.y == p3.y))


def create_new_matrix(rm, p):
    matrix = []
    for y in range(len(rm)):
        matrix.append([])
        for x in range(len(rm[y])):
            found = False
            for c in p:
                if x == c.x and y == c.y:
                    found = True
                    matrix[y].append(1000)
                    break
            if not found:
                matrix[y].append(rm[y][x])
    return np.array(matrix)


path_to_weight = []
for i in range(len(path)):
    if i > 1:
        if is_turn(path[i - 2], path[i - 1], path[i]):
            path_to_weight.append(path[i])

new_matrices = []
for i in range(len(path_to_weight)):
    new_matrices.append(create_new_matrix(raw_matrix, [path_to_weight[i]]))

new_matrices.append(create_new_matrix(raw_matrix, path_to_weight))

for new_matrix in new_matrices:
    n_turn = 0
    n_forward = 0
    prev_dir = 'R'
    old_x = 0
    old_y = 0
    diff_x = 0
    diff_y = 0
    grid = Grid(matrix=new_matrix)
    start = grid.node(start_x, start_y)
    end = grid.node(end_x, end_y)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
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
            n_forward += 1
            if prev_dir != cur_dir:
                n_turn += 1
            prev_dir = cur_dir
        old_x = x
        old_y = y
    print('=>', n_turn, n_forward, n_turn * 1000 + n_forward)
