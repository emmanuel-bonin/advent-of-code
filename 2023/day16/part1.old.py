# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

class Beam:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.direction = direction

class Tile:
  def __init__(self, x, y, t, max_x, max_y):
    self.x = x
    self.y = y
    self.max_x = max_x
    self.max_y = max_y
    self.type = t
    self.beams = []

  def __repr__(self):
    if len(self.beams) != 1:
      return self.type
    elif len(self.beams) == 1:
      if self.beams[0].direction == 'LEFT':
        return '<' if self.is_empty() else self.type
      elif self.beams[0].direction == 'RIGHT':
        return '>' if self.is_empty() else self.type
      elif self.beams[0].direction == 'UP':
        return '^' if self.is_empty() else self.type
      elif self.beams[0].direction == 'DOWN':
        return 'v' if self.is_empty() else self.type

  def energized():
    return True if len(self.beams) > 0 else False

  def is_empty(self):
    return True if '.' in self.type else False

  def is_mirror(self):
    return True if self.type == '\\' or self.type == '/' else False

  def is_splitter(self):
    return True if self.type == '-' or self.type == '|' else False

  def find_beam(self, direction):
    for b in self.beams:
      if b.direction == direction:
        return b
    return None

  def add_beam(self, direction):
    exisiting_beam = self.find_beam(direction)
    if exisiting_beam:
      print(self, 'at', self.x, self.y, '222 has already', direction)
      return []
    print('333 adding', direction, 'to', self, 'at', self.x, self.y)
    if self.is_empty():
      self.beams.append(Beam(self.x, self.y, direction))
    elif self.is_mirror():
      if direction == 'LEFT':
        if self.type == '\\' and self.y > 0:
          self.beams.append(Beam(self.x, self.y, 'UP'))
        elif self.type == '/' and self.y < self.max_y - 1:
          self.beams.append(Beam(self.x, self.y, 'DOWN'))
      elif direction == 'RIGHT':
        if self.type == '\\' and self.y < self.max_y - 1:
          self.beams.append(Beam(self.x, self.y, 'DOWN'))
        elif self.type == '/' and self.y > 0:
          self.beams.append(Beam(self.x, self.y, 'UP'))
      elif direction == 'UP':
        if self.type == '\\' and self.x > 0:
          self.beams.append(Beam(self.x, self.y, 'LEFT'))
        elif self.type == '/' and self.x < self.max_x - 1:
          self.beams.append(Beam(self.x, self.y, 'RIGHT'))
      elif direction == 'DOWN':
        if self.type == '\\' and self.x < self.max_x - 1:
          self.beams.append(Beam(self.x, self.y, 'RIGHT'))
        elif self.type == '/' and self.x > 0:
          self.beams.append(Beam(self.x, self.y, 'LEFT'))
    elif self.is_splitter():
      if direction == 'LEFT':
        if self.type == '-' and self.x > 0:
          self.beams.append(Beam(self.x, self.y, 'LEFT'))
        elif self.type == '|':
          if self.y > 0:
            self.beams.append(Beam(self.x, self.y, 'UP'))
          if self.y < self.max_y - 1:
            self.beams.append(Beam(self.x, self.y, 'DOWN'))
      elif direction == 'RIGHT':
        if self.type == '-' and self.x < self.max_x - 1:
          self.beams.append(Beam(self.x, self.y, 'RIGHT'))
        elif self.type == '|':
          if self.y > 0:
            self.beams.append(Beam(self.x, self.y, 'UP'))
          if self.y < self.max_y - 1:
            self.beams.append(Beam(self.x, self.y, 'DOWN'))
      elif direction == 'UP':
        if self.type == '-':
          if self.x > 0:
            self.beams.append(Beam(self.x, self.y, 'LEFT'))
          if self.x < self.max_x - 1:
            self.beams.append(Beam(self.x, self.y, 'RIGHT'))
        elif self.type == '|' and self.y > 0:
          self.beams.append(Beam(self.x, self.y, 'UP'))
      elif direction == 'DOWN':
        if self.type == '-':
          if self.x > 0:
            self.beams.append(Beam(self.x, self.y, 'LEFT'))
          if self.x < self.max_x - 1:
            self.beams.append(Beam(self.x, self.y, 'RIGHT'))
        elif self.type == '|' and self.y < self.max_y - 1:
          self.beams.append(Beam(self.x, self.y, 'DOWN'))
    return self.beams

class Grid:
  def __init__(self, size_y, size_x):
    self.size_x = size_x
    self.size_y = size_y
    self.tiles = [[]] * size_y
    self.start_beam = None

  def __repr__(self):
    s = ''
    for y in range(self.size_y):
      for x in range(self.size_x):
        s += self.tiles[y][x].__repr__()
      s += '\n'
    return s

  def add_tile(self, tile):
    if len(self.tiles[tile.y]) == 0:
      self.tiles[tile.y] = [None] * self.size_x
    self.tiles[tile.y][tile.x] = tile

  def set_start_beam(self, x, y, direction):
    self.start_beam = Beam(x, y, direction)

  def compute_beam(self):
    beams = [self.start_beam]
    finished = False
    while finished == False:
      # finished = True
      for i in range(len(beams)):
        print(self)
        b = beams[i]
        x = b.x
        y = b.y
        # beam_modified = False
        new_beams = self.tiles[y][x].add_beam(b.direction)
        beams = new_beams
        if b.direction == 'RIGHT':
        #   print('111 adding RIGHT')
        #   while x < self.size_x:
        #     new_beams = self.tiles[y][x].add_beam(b.direction)
        #     if self.tiles[y][x].type == '|' or self.tiles[y][x].type == '\\' or self.tiles[y][x].type == '/':
        #       del beams[i]
        #       beams += new_beams
        #       beam_modified = True
        #       break
        #     x += 1
        # elif b.direction == 'LEFT':
        #   print('111 adding LEFT')
        #   while x >= 0:
        #     new_beams = self.tiles[y][x].add_beam(b.direction)
        #     if self.tiles[y][x].type == '|' or self.tiles[y][x].type == '\\' or self.tiles[y][x].type == '/':
        #       del beams[i]
        #       beams += new_beams
        #       beam_modified = True
        #       break
        #     x -= 1
        # elif b.direction == 'UP':
        #   print('111 adding UP')
        #   while y >= 0:
        #     new_beams = self.tiles[y][x].add_beam(b.direction)
        #     if self.tiles[y][x].type == '-' or self.tiles[y][x].type == '\\' or self.tiles[y][x].type == '/':
        #       del beams[i]
        #       beams += new_beams
        #       beam_modified = True
        #       break
        #     y -= 1
        # elif b.direction == 'DOWN':
        #   print('111 adding DOWN')
        #   while y < self.size_y:
        #     new_beams = self.tiles[y][x].add_beam(b.direction)
        #     if self.tiles[y][x].type == '-' or self.tiles[y][x].type == '\\' or self.tiles[y][x].type == '/':
        #       del beams[i]
        #       beams += new_beams
        #       beam_modified = True
        #       break
        #     y += 1
        # if beam_modified == True:
        #   finished = False
        #   break

def main():
  max_y = 0
  max_x = 0
  grid = None
  lines = f.readlines()
  for y in range(len(lines)):
    lines[y] = lines[y].replace('\n', '').strip()
    if y == 0:
      max_y = len(lines)
      max_x = len(lines[0])
      grid = Grid(len(lines), len(lines[y]))
    for x in range(len(lines[y])):
      grid.add_tile(Tile(x, y, lines[y][x], max_x, max_y))
  grid.set_start_beam(0, 0, 'RIGHT')
  grid.compute_beam()
  print(grid)

if __name__ == "__main__":
  main()
