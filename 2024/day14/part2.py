def bot_at_pos(bots, x, y):
  for bot in bots:
    if bot[0] == x and bot[1] == y:
      return True
  return False

def print_map(bot_pos, width, height, sec):
  for i in range(height):
    buffer = ''
    for j in range(width):
      if bot_at_pos(bot_pos, j, i):
        buffer += '#'
      else:
        buffer += '.'
    n = 0
    for k in range(len(buffer)):
      if buffer[k] == '#':
        while k < len(buffer) and buffer[k] == '#':
          k += 1
          n += 1
        if n >= 10:
          print('Found more than 10 continguous # at sec:', sec, 'at')
          print('n:', n, buffer)
        k += n
        n = 0

def main():
#   f = open('example.txt', 'r')
  f = open('input.txt', 'r')
  width, height = 0,   0
  n_sec = 1000
  bots = []
  for line in f.readlines():
    if line.startswith('p='):
      p = [int(line.split(' ')[0].split('=')[1].split(',')[0]), int(line.split(' ')[0].split('=')[1].split(',')[1])]
      v = [int(line.split(' ')[1].split('=')[1].split(',')[0]), int(line.split(' ')[1].split('=')[1].split(',')[1])]
      x = p[0]
      y = p[1]
      bots.append([x, y, v])
    else:
      width = int(line.split(',')[0])
      height = int(line.split(',')[1])
  sec = 0
  while True:
    sec += 1
    for j in range(len(bots)):
      bots[j][0] += (bots[j][2][0]) % width
      bots[j][0] %= width
      bots[j][1] += (bots[j][2][1]) % height
      bots[j][1] %= height
    print_map(bots, width, height, sec)
main()
