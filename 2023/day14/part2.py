import math

f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

platform = {
  'round': [],
  'square': [],
}

platform_raw = []
n_lines = 0
line_len = 0
for l in lines:
  l = l.replace('\n', '').strip()
  platform_raw.append(l)
  line_len = len(l)
  n_lines += 1

ids = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
n = 0
for y in range(len(platform_raw)):
  for x in range(len(platform_raw[y])):
    if platform_raw[y][x] == 'O':
      platform['round'].append({
        'x': x,
        'y': y,
        'n': ids[n % 25]
      })
      n += 1
    elif platform_raw[y][x] == '#':
      platform['square'].append({
        'x': x,
        'y': y
      })

def print_platform(p):
  for y in range(n_lines):
    s = ''
    for x in range(line_len):
      round_rocks = [i for i in p['round'] if i['x'] == x and i['y'] == y]
      square_rocks = [i for i in p['square'] if i['x'] == x and i['y'] == y]
      if len(round_rocks) == 0 and len(square_rocks) == 0:
        s += '.'
      elif len(round_rocks) == 0 and len(square_rocks) != 0:
        s += '#'
      elif len(round_rocks) != 0 and len(square_rocks) == 0:
        s += 'O'
    print(s)

def tilt_platform_north(p):
  p['round'] = sorted(p['round'], key=lambda x: x['y'])
  finished = False
  while finished == False:
    for r in p['round']:
      finished = True
      if r['y'] == 0:
        continue
      rocks_north = sorted(list(filter(lambda rock: rock['y'] < r['y'] and rock['x'] == r['x'], p['square'])) + list(filter(lambda rock: rock['y'] < r['y'] and rock['x'] == r['x'], p['round'])), key=lambda rock: rock['y'], reverse=True)
      if len(rocks_north) == 0:
        if r['y'] != 0:
          finished = False
          r['y'] = 0
      else:
        if r['y'] != rocks_north[0]['y'] + 1:
          finished = False
          r['y'] = rocks_north[0]['y'] + 1

def tilt_platform_west(p):
  p['round'] = sorted(p['round'], key=lambda x: x['x'])
  finished = False
  while finished == False:
    finished = True
    for r in p['round']:
      if r['x'] == 0:
        continue
      rocks_west = sorted(list(filter(lambda rock: rock['x'] < r['x'] and rock['y'] == r['y'], p['square'])) + list(filter(lambda rock: rock['x'] < r['x'] and rock['y'] == r['y'], p['round'])), key=lambda rock: rock['x'], reverse=True)
      if len(rocks_west) == 0:
        if r['x'] != 0:
          finished = False
          r['x'] = 0
      else:
        if r['x'] != rocks_west[0]['x'] + 1:
          finished = False
          r['x'] = rocks_west[0]['x'] + 1

def tilt_platform_east(p):
  p['round'] = sorted(p['round'], key=lambda x: x['x'], reverse=True)
  finished = False
  while finished == False:
    finished = True
    for r in p['round']:
      if r['x'] == line_len - 1:
        continue
      rocks_east = sorted(list(filter(lambda rock: rock['x'] > r['x'] and rock['y'] == r['y'], p['square'])) + list(filter(lambda rock: rock['x'] > r['x'] and rock['y'] == r['y'], p['round'])), key=lambda rock: rock['x'])
      if len(rocks_east) == 0:
        if r['x'] != line_len - 1:
          finished = False
          r['x'] = line_len - 1
      else:
        if r['x'] != rocks_east[0]['x'] - 1:
          finished = False
          r['x'] = rocks_east[0]['x'] - 1

def tilt_platform_south(p):
  p['round'] = sorted(p['round'], key=lambda x: x['y'], reverse=True)
  finished = False
  while finished == False:
    finished = True
    for r in p['round']:
      if r['y'] == n_lines - 1:
        continue
      rocks_south = sorted(list(filter(lambda rock: rock['y'] > r['y'] and rock['x'] == r['x'], p['square'])) + list(filter(lambda rock: rock['y'] > r['y'] and rock['x'] == r['x'], p['round'])), key=lambda rock: rock['y'])
      if len(rocks_south) == 0:
        if r['y'] != n_lines - 1:
          finished = False
          r['y'] = n_lines - 1
      else:
        if r['y'] != rocks_south[0]['y'] - 1:
          finished = False
          r['y'] = rocks_south[0]['y'] - 1

def cycle(platform):
  tilt_platform_north(platform)
  tilt_platform_west(platform)
  tilt_platform_south(platform)
  tilt_platform_east(platform)

def platform_to_str(p):
  result_str = ''
  for y in range(n_lines):
    s = ''
    for x in range(line_len):
      round_rocks = [i for i in p['round'] if i['x'] == x and i['y'] == y]
      square_rocks = [i for i in p['square'] if i['x'] == x and i['y'] == y]
      if len(round_rocks) == 0 and len(square_rocks) == 0:
        s += '.'
      elif len(round_rocks) == 0 and len(square_rocks) != 0:
        s += '#'
      elif len(round_rocks) != 0 and len(square_rocks) == 0:
        s += 'O'
    result_str += s + '\n'
  return result_str

def compute_platform(platform):
  res = 0
  for r in platform['round']:
    res += n_lines - r['y']
  return res

result_patterns = {}
loop_size = 0
start_of_loop = 0
loop_elements = []
CYCLES = 1000000000
for i in range(CYCLES):
  cycle(platform)
  p_str = platform_to_str(platform)
  if p_str not in result_patterns:
    result_patterns[p_str] = platform
  else:
    start_of_loop = i + 1
    loop_elements.append(compute_platform(platform))
    for j in range(CYCLES):
      cycle(platform)
      loop_size += 1
      p_str2 = platform_to_str(platform)
      if p_str2 == p_str:
        print('loop size', loop_size)
        break
      else:
        loop_elements.append(compute_platform(platform))
    break
  print(i+1, 'cycle')
print('loop start at', start_of_loop, 'with size', loop_size)
print(loop_elements)

print(loop_elements[(CYCLES - start_of_loop) % loop_size])
