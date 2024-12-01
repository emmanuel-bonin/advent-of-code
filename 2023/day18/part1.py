from shapely.geometry import Point, Polygon

# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

lines = f.readlines()

res = 0

corners = list()
start = Point(0, 0)
corners.append(start)
start_x = 0
end_x = 0
start_y = 0
end_y = 0

for l in lines:
  l = l.replace('\n', '').strip()
  current = corners[-1]
  coord = l.split(' ')[:2]
  if coord[0] == 'R':
    corners.append(Point(current.x + int(coord[1]), current.y))
    end_x = int(max(end_x, current.x + int(coord[1])))
    res += int(coord[1])
  elif coord[0] == 'D':
    corners.append(Point(current.x, current.y + int(coord[1])))
    end_y = int(max(end_y, current.y + int(coord[1])))
    res += int(coord[1])
  elif coord[0] == 'L':
    corners.append(Point(current.x - int(coord[1]), current.y))
    start_x = int(min(start_x, current.x - int(coord[1])))
    res += int(coord[1])
  elif coord[0] == 'U':
    corners.append(Point(current.x, current.y - int(coord[1])))
    start_y = int(min(start_y, current.y - int(coord[1])))
    res += int(coord[1])

poly = Polygon(corners)
for y in range(start_y, end_y):
  for x in range(start_x, end_x):
    if poly.contains(Point(x, y)):
      res += 1
print(res)
