# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

def main():
  max_y = 0
  max_x = 0
  grid = []
  lines = f.readlines()
  for y in range(len(lines)):
    lines[y] = lines[y].replace('\n', '').strip()
    if y == 0:
      max_y = len(lines)
      max_x = len(lines[0])
    row = []
    for x in range(len(lines[y])):
      row.append({ 'x': x, 'y': y, 'type': lines[y][x] })
    grid.append(row)
  print(grid)

if __name__ == "__main__":
  main()
