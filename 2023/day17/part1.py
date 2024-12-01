from heapq import *

# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

lines = f.readlines()

matrix = [[int(char) for char in row.replace('\n', '').strip()] for row in lines]


class Point:
  def __init__(self, row=0, col=0):
    self.row = row
    self.col = col

  def __eq__(self, a):
    return self.col == a.col and self.row == a.row

  def __add__(self, a):
    return Point(self.row + a.row, self.col + a.col)

  def __repr__(self):
    return f'[{self.row} {self.col}]'

class State:
  def __init__(self):
    self.position = Point(0, 0)
    self.direction = 0
    self.moves = 0
    self.heat_loss = 0

  def __lt__(self, a):
    return self.heat_loss < a.heat_loss

  def __eq__(self, other):
    return self.position == other.position and self.moves == other.moves and self.direction == other.direction

  def __repr__(self):
    d = 'RIGHT' if self.direction == 1 else 'DOWN' if self.direction == 2 else 'LEFT' if self.direction == 3 else 'UP'
    return f'{self.position}: Direction {d} {self.heat_loss}'

  def __hash__(self):
    return self.position.row + self.position.col

def in_map_limits(state):
  return True if state.position.col >= 0 and state.position.col < len(matrix[0]) and state.position.row >= 0 and state.position.row < len(matrix) else False

destination = Point(len(matrix[0]) - 1, len(matrix) - 1)

pq = list()
seen = set()

state = State()
state.direction = 1
heappush(pq, state)

state = State()
state.direction = 2
heappush(pq, state)

motions = [
  Point(-1, 0),
  Point(0, 1),
  Point(1, 0),
  Point(0, -1)
]

while len(pq):
  state = heappop(pq)

  if state in seen:
    continue

  seen.add(state)

  if state.position == destination:
    print(state.heat_loss)
    exit(0)

  new_state = State()
  new_state.direction = (state.direction - 1 + 4) % 4
  new_state.position = state.position + motions[new_state.direction]
  if in_map_limits(new_state):
    new_state.heat_loss = state.heat_loss + matrix[new_state.position.row][new_state.position.col]
    new_state.moves = 0
    heappush(pq, new_state)

  new_state = State()
  new_state.direction = (state.direction + 1 + 4) % 4
  new_state.position = state.position + motions[new_state.direction]
  if in_map_limits(new_state):
    new_state.heat_loss = state.heat_loss + matrix[new_state.position.row][new_state.position.col]
    new_state.moves = 0
    heappush(pq, new_state)

  if state.moves < 2:
    new_state = State()
    new_state.direction = state.direction
    new_state.position = state.position + motions[new_state.direction]
    if in_map_limits(new_state):
      new_state.heat_loss = state.heat_loss + matrix[new_state.position.row][new_state.position.col]
      new_state.moves = state.moves + 1
      heappush(pq, new_state)
