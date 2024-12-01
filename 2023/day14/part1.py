
f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

platform = {
  'round': [],
  'square': [],
}

platform_raw = []
n_lines = 0
for l in lines:
  l = l.replace('\n', '').strip()
  platform_raw.append(l)
  n_lines += 1

for y in range(len(platform_raw)):
  for x in range(len(platform_raw[y])):
    if platform_raw[y][x] == 'O':
      platform['round'].append({
        'x': x,
        'y': y
      })
    elif platform_raw[y][x] == '#':
      platform['square'].append({
        'x': x,
        'y': y
      })

def tilt_platform(p):
  for r in p['round']:
    if r['y'] == 0:
      continue
    squares_north = list(filter(lambda rock: rock['y'] < r['y'] and rock['x'] == r['x'], p['round']))
    rounds_north = list(filter(lambda rock: rock['y'] < r['y'] and rock['x'] == r['x'], p['square']))
    if len(squares_north) == 0 and len(rounds_north) == 0:
      r['y'] = 0
    elif len(squares_north) == 0 and len(rounds_north) != 0:
      r['y'] = rounds_north[-1]['y'] + 1
    elif len(squares_north) != 0 and len(rounds_north) == 0:
      r['y'] = squares_north[-1]['y'] + 1
    else:
      r['y'] = max(squares_north[-1]['y'], rounds_north[-1]['y']) + 1

tilt_platform(platform)
res = 0
for r in platform['round']:
  res += n_lines - r['y']
print(res)
