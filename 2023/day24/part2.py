from sympy import Line, Point, Ray
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Hailstone:
  def __init__(self, pos, vel):
    self.pos = pos
    self.vel = vel

  def compute_end(self, time):
    return Line(Point(self.pos[0], self.pos[1], self.pos[2]), Point(self.pos[0] + self.vel[0] * time, self.pos[1] + self.vel[1] * time, self.pos[2] + self.vel[2] * time))

  def compute_ray(self):
    return Ray(self.pos, Point(self.pos[0] + self.vel[0], self.pos[1] + self.vel[1], self.pos[2] + self.vel[2]))

def main():
  # f = open('./input.txt', 'r')
  f = open('./example.txt', 'r')
  lines = f.readlines()
  stones = []
  for l in lines:
    l = l.replace('\n', '').strip()
    arr = l.split('@')
    posArr = list(map(lambda x: int(x), arr[0].split(',')))
    velArr = list(map(lambda x: int(x), arr[1].split(',')))
    stones.append(Hailstone((posArr[0], posArr[1], posArr[2]), (velArr[0], velArr[1], velArr[2])))

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  def update(i):
    ax.clear()
    for s in stones:
      l = s.compute_end(i+1)
      ax.plot([l.p1.x, l.p2.x], [l.p1.y, l.p2.y], zs=[l.p1.z, l.p2.z])
  a = anim.FuncAnimation(fig, update, frames=20000, repeat=False)
  plt.show()


if __name__ == "__main__":
  main()
