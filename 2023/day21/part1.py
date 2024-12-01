class Case:
  def __init__(self, row, col, type):
    self.row = row
    self.col = col
    self.type = '.' if type == '.' or type == 'S' else '#'
    self.is_start = type == 'S'

  def __str__(self):
    return self.type

class Grid:
  def __init__(self, nb_rows, nb_cols):
    self.nb_rows = nb_rows
    self.nb_cols = nb_cols
    self.tiles = [[]] * nb_rows
    self.possibilities = []
    for i in range(self.nb_rows):
      self.tiles[i] = [None] * nb_cols
    self.steps = 0

  def __str__(self):
    s = ''
    for i in range(self.nb_rows):
      for j in range(self.nb_cols):
        possibility = list(filter(lambda x: x.col == j and x.row == i and x.type != 'S', self.possibilities))
        if self.tiles[i][j].is_start:
          s += 'S'
        elif len(possibility):
          s += 'O'
        else:
          s += self.tiles[i][j].type
      s += '\n'
    return s

  def add_case(self, row, col, type):
    case = Case(row, col, type)
    self.tiles[row][col] = case
    if type == 'S':
      self.start = case
      self.possibilities.append(case)

  def add_step(self):
    new_possibilities = []
    finished = False
    while finished == False:
      finished = True
      for i in range(len(self.possibilities)):
        row = self.possibilities[i].row
        col = self.possibilities[i].col
        if col > 0 and self.tiles[row][col-1].type == '.':
          if self.tiles[row][col-1] not in new_possibilities:
            new_possibilities.append(self.tiles[row][col-1])
          finished = False
        if col < self.nb_cols-1 and self.tiles[row][col+1].type == '.':
          if self.tiles[row][col+1] not in new_possibilities:
            new_possibilities.append(self.tiles[row][col+1])
          finished = False
        if row > 0 and self.tiles[row-1][col].type == '.':
          if self.tiles[row-1][col] not in new_possibilities:
            new_possibilities.append(self.tiles[row-1][col])
          finished = False
        if row < self.nb_rows-1 and self.tiles[row+1][col].type == '.':
          if self.tiles[row+1][col] not in new_possibilities:
            new_possibilities.append(self.tiles[row+1][col])
          finished = False
        if finished == False:
          del self.possibilities[i]
          break
    self.possibilities = new_possibilities
    self.steps += 1
    pass

def main():
  f = open('./input.txt', 'r')
  # f = open('./example.txt', 'r')

  lines = f.readlines()
  grid = Grid(len(lines), len(lines[0].replace('\n', '').strip()))
  for row in range(len(lines)):
    l = lines[row]
    l = l.replace('\n', '').strip()
    for col in range(len(l)):
      grid.add_case(row, col, l[col])
  for _ in range(64):
    grid.add_step()
    # print(grid)
  print(len(grid.possibilities))

if __name__ == "__main__":
  main()
