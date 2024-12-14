def main():
#   f = open('example.txt', 'r')
  f = open('input.txt', 'r')
  width, height = 0, 0
  n_sec = 100
  res1 = 0
  res2 = 0
  res3 = 0
  res4 = 0
  for line in f.readlines():
    if line.startswith('p='):
      p = [int(line.split(' ')[0].split('=')[1].split(',')[0]), int(line.split(' ')[0].split('=')[1].split(',')[1])]
      v = [int(line.split(' ')[1].split('=')[1].split(',')[0]), int(line.split(' ')[1].split('=')[1].split(',')[1])]
      x = (p[0] + v[0] * n_sec) % width
      y = (p[1] + v[1] * n_sec) % height
      if x != int(width / 2) and y != int(height / 2):
        res1 += 1 if x < int(width / 2) and y < int(height / 2) else 0
        res2 += 1 if x > int(width / 2) and y < int(height / 2) else 0
        res3 += 1 if x < int(width / 2) and y > int(height / 2) else 0
        res4 += 1 if x > int(width / 2) and y > int(height / 2) else 0

    else:
      width = int(line.split(',')[0])
      height = int(line.split(',')[1])
  print(res1 * res2 * res3 * res4)

main()
