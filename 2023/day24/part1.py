from sympy import Ray, Point

MIN_POS = 200000000000000
MAX_POS = 400000000000000
# MIN_POS = 7
# MAX_POS = 27

class Hailstone:
  def __init__(self, pos, vel):
    self.pos = pos
    self.vel = vel

def compute_ray(stone):
  return Ray(Point(stone.pos[0], stone.pos[1]), Point(stone.pos[0] + stone.vel[0], stone.pos[1] + stone.vel[1]))

def main():
  f = open('./input.txt', 'r')
  # f = open('./example.txt', 'r')
  lines = f.readlines()
  stones = []
  for l in lines:
    l = l.replace('\n', '').strip()
    arr = l.split('@')
    posArr = list(map(lambda x: int(x), arr[0].split(',')))
    velArr = list(map(lambda x: int(x), arr[1].split(',')))
    stones.append(Hailstone((posArr[0], posArr[1], posArr[2]), (velArr[0], velArr[1], velArr[2])))
  print('Initialized', len(stones), 'stones')
  result = 0
  for i in range(len(stones)):
    print('computing collisions for stone', i)
    for j in range(i+1, len(stones)):
      ray1 = compute_ray(stones[i])
      ray2 = compute_ray(stones[j])
      intersect = ray1.intersection(ray2)
      if len(intersect):
        intersect_point = intersect[0]
        if float(intersect_point.x) >= MIN_POS and float(intersect_point.x) <= MAX_POS and float(intersect_point.y) >= MIN_POS and float(intersect_point.y) <= MAX_POS:
          result += 1
  print(result)

if __name__ == "__main__":
  main()
