from shapely.geometry import Point, Polygon

f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

res = 0

corners = list()
start = (0, 0)
corners.append(start)

# additional will contain all the holes around the polygon area to add to the result of the library
# but idk why, needed to divide it by 2 and add 1 🤷
additional = 0

for l in lines:
  l = l.replace('\n', '').strip()
  hex = l.replace(')', '').split('#')[1]
  direction = 'R' if hex[-1] == '0' else 'D' if hex[-1] == '1' else 'L' if hex[-1] == '2' else 'U'
  num = int(hex[:5], 16)
  current = corners[-1] if len(corners) else start

  additional += num
  if direction == 'R':
    corners.append((current[0] + num, current[1]))
  elif direction == 'D':
    corners.append((current[0], current[1] + num))
  elif direction == 'L':
    corners.append((current[0] - num, current[1]))
  elif direction == 'U':
    corners.append((current[0], current[1] - num))

poly = Polygon(corners)
print(additional / 2 + 1)
print(int(poly.area) + int(additional / 2 + 1))

# 6405262 / 2 = 3202631
# 952408144115 - 952404941483 = 3202632
# 952408144115
