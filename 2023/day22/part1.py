from heapq import *
from sympy import Line, Point

# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

l1 = Line(Point(0, 0, 1), Point(2, 2, 1))
l2 = Line(Point(0, 0, 2), Point(2, 2, 4))
print(l1.intersection(l2))
exit(0)

class Brick:
  def __init__(self, start, end):
    self.p1 = start
    self.p2 = end
    self.p = start
    self.v = (end[0] - start[0], end[1] - start[1], end[2] - start[2])

  def __lt__(self, other):
    return min(self.p2[2], self.p2[2]) < min(other.p2[2], other.p2[2])

  def __repr__(self):
    return f'p1: [{self.p1[0]} {self.p1[1]} {self.p1[2]}] => p2: [{self.p2[0]} {self.p2[1]} {self.p2[2]}]'

  def go_downward(self):
    self.p1 = (self.p1[0], self.p1[1], self.p1[2] - 1)
    self.p2 = (self.p2[0], self.p2[1], self.p2[2] - 1)
    self.p = (self.p[0], self.p[1], self.p[2] - 1)

def main():
  lines = f.readlines()
  bricks = list()
  for l in lines:
    l = l.replace('\\n', '').strip()
    start_end = l.split('~')
    start = tuple(map(lambda x: int(x), start_end[0].split(',')))
    end = tuple(map(lambda x: int(x), start_end[1].split(',')))
    heappush(bricks, Brick(start, end))
  settled = list()
  for b in bricks:
    print(b.p1, b.p2)
  # while there are falling bricks
  while len(bricks) > 0:
    # Get the lowest falling brick
    brick = heappop(bricks)
    # If not brick has been settled, we settle the first one
    if len(settled) == 0:
      heappush(settled, brick)
    else:
      collision_found = False
      finished = False
      while finished == False:
        finished = True
        # iterating over already settled bricks and look for collision with current brick but with a lower 1 z
        for s in list(reversed(settled)):
          line1 = Line(Point(s.p1), Point(s.p2))
          line2 = Line(Point((brick.p1[0], brick.p1[1], brick.p1[2] - 1)), Point((brick.p2[0], brick.p2[1], brick.p2[2] - 1)))
          intersect = line1.intersection(line2)
          if intersect:
            print('Collision found between settled', s, 'and brick', brick, 'at', intersect)
            collision_found = True
            break
          else:
            print('No collision between settled', s, 'and brick', brick)
        # if no collision has been found
        if collision_found == False:
          # make the brick fall 1 on z if it is above ground
          if brick.p2[2] > 1:
            print('Brick', brick, 'going downward')
            brick.go_downward()
            finished = False
            continue
          # if it is at ground level, let's settle it
          else:
            heappush(settled, brick)
        # if a collision is found, settle it
        else:
          heappush(settled, brick)
          break
  for b in settled:
    # bricks_above = settled.find()
    print('-->', b.p1, b.p2)

if __name__ == "__main__":
  main()
