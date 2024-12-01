from math import sqrt

f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

def print_map(m):
  for i in range(len(m)):
    print(m[i])

initial_map = list()
for l in lines:
  l = l.replace('\n', '').strip()
  initial_map.append(l)

# Expanding the map
empty_line = ''
for j in range(len(initial_map[0])):
  empty_line += '.'
lines_to_add_idx = list()
for i in range(len(initial_map)):
  if '#' not in initial_map[i]:
    lines_to_add_idx.append(i)
inserted_rows = 0
for i in range(len(lines_to_add_idx)):
  initial_map.insert(lines_to_add_idx[i]+inserted_rows, empty_line)
  inserted_rows += 1
col_to_add_idx = list()
inserted_cols = 0
line_len = len(initial_map[0])
for i in range(line_len):
  galaxy_in_column = False
  for j in range(len(initial_map)):
    if initial_map[j][i] == '#':
      galaxy_in_column = True
      break
  if galaxy_in_column == False:
    col_to_add_idx.append(i)
for i in col_to_add_idx:
  for j in range(len(initial_map)):
    idx = i+inserted_cols
    initial_map[j] = initial_map[j][:idx] + '.' + initial_map[j][idx:]
  inserted_cols += 1

# Settings IDs to galaxies
cpt = 1
galaxies = list()
for i in range(len(initial_map)):
  for j in range(len(initial_map[i])):
    if initial_map[i][j] == '#':
      galaxies.append(dict({ 'x': j, 'y': i, 'id': cpt }))
      cpt += 1

print_map(initial_map)
print_map(galaxies)

def compute_path(g1, g2):
  x1 = abs(g1['x'])
  x2 = abs(g2['x'])
  y1 = abs(g1['y'])
  y2 = abs(g2['y'])
  diff_x = abs(x2 - x1)
  diff_y = abs(y2 - y1)
  return diff_x + diff_y

res = 0
for i in range(len(galaxies)):
  for j in range(i + 1, len(galaxies)):
    d = compute_path(galaxies[i], galaxies[j])
    res += d

print(res)
