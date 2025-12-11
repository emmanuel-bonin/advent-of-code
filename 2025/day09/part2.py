import math

f = open('input.txt', 'r')
lines = [line.strip() for line in f.readlines()]
f.close()

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

# tiles = set()
tiles = list()
max_x = 0
max_y = 0
for i, _ in enumerate(lines):
    [x, y] = [int(s) for s in lines[i].split(',')]
    # tiles.add(Tile(x, y, 'r'))
    tiles.append(Tile(x, y, 'r'))
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

def print_map(map: list[Tile], others: list[Tile]):
    s = ''
    for y in range(max_y + 2):
        for x in range(max_x + 3):
            tile = Tile(x, y)
            found = False
            for o in others:
                if o == tile:
                    found = True
                    s += "O"
            if not found:
                for t in map:
                    if tile == t:
                        found = True
                        s += "#" if t.color == "r" else "X" if t.color == "g" else ""
            if not found:
                s += '.'
        s += '\n'
    print(s)

tiles_x_by_y = {}
# def inside_polygon(tile: Tile) -> bool:
#     cpt = 0
#     if tiles_x_by_y.get(tile.y) is None:
#         return False
#     listx = list(tiles_x_by_y.get(tile.y))
#     for _, x in enumerate(listx):
#         if x >= tile.x:
#             cpt += 1
#     return False if cpt % 2 == 0 else True

def add_tiles_x_by_y(x, y):
    if tiles_x_by_y.get(y) is None:
        tiles_x_by_y[y] = set()
    tiles_x_by_y[y].add(x)

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
    return new_tiles

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

cache = {}
def tile_in_polygon(tile: Tile, polygon: list[Tile]):
    if tile in cache:
        return cache[tile]
    num_vertices = len(polygon)
    x, y = tile.x, tile.y
    inside = False

    # Store the first tile in the polygon and initialize the second tile
    tile1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next tile in the polygon
        tile2 = polygon[i % num_vertices]

        # Check if the tile is above the minimum y coordinate of the edge
        if y > min(tile1.y, tile2.y):
            # Check if the tile is below the maximum y coordinate of the edge
            if y <= max(tile1.y, tile2.y):
                # Check if the tile is to the left of the maximum x coordinate of the edge
                if x <= max(tile1.x, tile2.x):
                    # Calculate the x-intersection of the line connecting the tile to the edge
                    x_intersection = (y - tile1.y) * (tile2.x - tile1.x) / (tile2.y - tile1.y) + tile1.x

                    # Check if the tile is on the same line as the edge or to the left of the x-intersection
                    if tile1.x == tile2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current tile as the first tile for the next iteration
        tile1 = tile2

    # Return the value of the inside flag
    cache[tile] = inside
    return inside

# corner_tiles = list(tiles)

print('adding contour...')
contour = add_contour()
print('contour added. generating and checking rectangles in', len(tiles), 'tiles')

largest_area = 0
tiles_list = list(tiles)
contour_list = list(contour)
full_list = list(tiles)
full_list.extend(contour)
points_to_test = []
for i, t1 in enumerate(tiles):
    for j, t2 in enumerate(tiles):
        if i == j or t1.color != 'r' or t2.color != 'r':
            continue

        sx = min(t1.x, t2.x)
        sy = min(t1.y, t2.y)
        ex = max(t1.x, t2.x)
        ey = max(t1.y, t2.y)

        abort = False
        x = sx
        while x <= ex:
            y = sy
            while y <= ey:
                new_t = Tile(x, y)
                if new_t in tiles or new_t in contour or tile_in_polygon(new_t, tiles_list):
                    # print("Point", new_t, "is inside the polygon")
                    pass
                else:
                    # print('found a point', new_t, 'of rect', t1, t2, 'not in polygon')
                    # if new_t not in points_to_test:
                    #     points_to_test.append(new_t)
                    abort = True
                    break
                y += 1
            if abort:
                break
            x += 1

        if abort:
            continue

        area = (abs(t1.x - t2.x) + 1) * (abs(t1.y - t2.y) + 1)
        if area > largest_area:
            # print('rect', t1, t2, 'in polygon. area =', area)
            largest_area = area

# print_map(full_list, points_to_test)
# print(points_to_test)
print(largest_area)
