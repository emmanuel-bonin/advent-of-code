import math
from threading import Thread
# import time

f = open('example.txt', 'r')
lines = [line.strip() for line in f.readlines()]
f.close()

# class ThreadWithReturnValue(Thread):
#     def __init__(
#         self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
#     ):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#
#     def run(self):
#         if self._target is not None:
#             self._return = self._target(*self._args, **self._kwargs)
#
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return


class Tile:
    def __init__(self, x, y, color='u'):
        self.x = x
        self.y = y
        self.color = color
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f'({self.x}, {self.y})'
    def __hash__(self):
        return hash((self.x, self.y))

tiles = set()
max_x = 0
max_y = 0
for i, _ in enumerate(lines):
    [x, y] = [int(s) for s in lines[i].split(',')]
    tiles.add(Tile(x, y, 'r'))
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

def print_map():
    s = ''
    for y in range(max_y + 2):
        for x in range(max_x + 3):
            tile = Tile(x, y)
            found = False
            for t in tiles:
                if tile == t:
                    found = True
                    s += '#' if t.color == 'r' else 'X' if t.color == 'g' else ''
            if not found:
                s += '.'
        s += '\n'
    print(s)

tiles_x_by_y = {}
def inside_polygon(tile: Tile) -> bool:
    cpt = 0
    if tiles_x_by_y.get(tile.y) is None:
        return False
    listx = list(tiles_x_by_y.get(tile.y))
    for _, x in enumerate(listx):
        if x >= tile.x:
            cpt += 1
    return False if cpt % 2 == 0 else True

def add_tiles_x_by_y(x, y):
    if tiles_x_by_y.get(y) is None:
        tiles_x_by_y[y] = set()
    tiles_x_by_y[y].add(x)
#
def find_adjacent_tiles(tile: Tile):
    adj = []
    for t in tiles:
        if t == tile or (t.x != tile.x and t.y != tile.y):
            continue
        if t.x == tile.x:
            adj.append(t)
        elif t.y == tile.y:
            adj.append(t)
    if len(adj) > 2:
        adj_by_dist = {}
        distances = []
        for t in adj:
            dist = int(math.sqrt(math.pow(t.x - tile.x, 2) + math.pow(t.y - tile.y, 2)))
            distances.append(dist)
            adj_by_dist[dist] = t
        distances.sort()
        adj = [adj_by_dist[distances[0]], adj_by_dist[distances[1]]]
    return adj

def add_contour():
    new_tiles = set()
    for tile in tiles:
        add_tiles_x_by_y(tile.x, tile.y)

        adjacent_tiles = find_adjacent_tiles(tile)
        for adj_tile in adjacent_tiles:
            diffx = adj_tile.x - tile.x
            diffy = adj_tile.y - tile.y
            if diffx > 0:
                x = tile.x + 1
                while x < adj_tile.x:
                    new_tile = Tile(x, tile.y, 'g')
                    add_tiles_x_by_y(x, tile.y)
                    new_tiles.add(new_tile)
                    x+=1
            elif diffx < 0:
                x = tile.x - 1
                while x > adj_tile.x:
                    new_tile = Tile(x, tile.y, "g")
                    add_tiles_x_by_y(x, tile.y)
                    new_tiles.add(new_tile)
                    x -= 1
            elif diffy > 0:
                y = tile.y + 1
                while y < adj_tile.y:
                    new_tile = Tile(tile.x, y, "g")
                    add_tiles_x_by_y(tile.x, y)
                    new_tiles.add(new_tile)
                    y += 1
            elif diffy < 0:
                y = tile.y - 1
                while y > adj_tile.y:
                    new_tile = Tile(tile.x, y, "g")
                    add_tiles_x_by_y(tile.x, y)
                    new_tiles.add(new_tile)
                    y -= 1
    tiles.update(new_tiles)

corner_tiles = list(tiles)

print('adding contour...')
add_contour()
print('contour added. generating and checking rectangles in', len(tiles), 'tiles')

# cache = {}
# def is_pos_in_polygon(x, y) -> bool:
#     new_t = Tile(x, y)
#
#     if cache.get(new_t) is not None:
#         return cache.get(new_t)
#
#     in_tiles = new_t in tiles
#
#     if not in_tiles:
#         in_poly = inside_polygon(new_t)
#         if not in_poly:
#             cache[new_t] = False
#             return False
#     cache[new_t] = True
#     return True
#
# def is_x_line_in_polygon(sx, ex, y) -> bool:
#     for x in range(sx, ex):
#         if not is_pos_in_polygon(x, y):
#             return False
#     return True
#
# def is_y_line_in_polygon(sy, ey, x) -> bool:
#     for y in range(sy, ey):
#         if not is_pos_in_polygon(x, y):
#             return False
#     return True

def tile_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point.x, point.y
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1.y, p2.y):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1.y, p2.y):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1.x, p2.x):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1.x == p2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    # Return the value of the inside flag
    return inside

largest_area = 0
for i, t1 in enumerate(corner_tiles):
    # print("generating rectangle for tiles i =", i, "/", len(corner_tiles), '=>', int(i/len(corner_tiles)*100), '%')
    for j, t2 in enumerate(corner_tiles):
        # print("generating rectangle", i*len(corner_tiles)+j, "/", len(corner_tiles)*(len(corner_tiles)-1), "=>", (i*len(corner_tiles)+j) / (len(corner_tiles)*(len(corner_tiles)-1)) * 100, "%")
        if i == j or t1.color != 'r' or t2.color != 'r':
            continue

        sx = min(t1.x, t2.x)
        sy = min(t1.y, t2.y)
        ex = max(t1.x, t2.x)
        ey = max(t1.y, t2.y)

        area = (abs(t1.x - t2.x) + 1) * (abs(t1.y - t2.y) + 1)

        abort = False
        for x in range(sx, ex):
            for y in range(sy, ey):
                new_t = Tile(x, y)
                if new_t not in tiles and not tile_in_polygon(new_t, corner_tiles):
                    print('found a point', new_t, 'of rect', t1, t2, 'not in polygon')
                    abort = True
                    break
            if abort:
                break

        if abort:
            continue

        if area > largest_area:
            print('rect', t1, t2, 'in polygon. area =', area)
            largest_area = area

print_map()
print(largest_area)
