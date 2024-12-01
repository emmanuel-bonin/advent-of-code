f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

# EXP=100
EXP=1000000

def print_map(m, empty_rows=[], empty_cols=[]):
  for i in range(len(m)):
    print(m[i])

initial_map = list()
for l in lines:
  l = l.replace('\n', '').strip()
  initial_map.append(l)

# Expanding the map

# Computing indexes where to insert new rows
empty_row_idx = list()
for i in range(len(initial_map)):
  # searching for a galaxy in current row
  if '#' not in initial_map[i]:
    empty_row_idx.append(i)
# computing column indexes where to insert new empty col
empty_col_idx = list()
# iterating over each rows
for i in range(len(initial_map[0])):
  # try to find a galaxy in current column
  galaxy_in_column = False
  for j in range(len(initial_map)):
    if initial_map[j][i] == '#':
      galaxy_in_column = True
      break
  # if no galaxy in column, add an empty col
  if galaxy_in_column == False:
    empty_col_idx.append(i)

# Settings IDs to galaxies
cpt = 1
galaxies = list()
found_empty_rows = 0
for i in range(len(initial_map)):
  if i in empty_row_idx:
    found_empty_rows += 1
  found_empty_cols = 0
  for j in range(len(initial_map[i])):
    if j in empty_col_idx:
      found_empty_cols += 1
    if initial_map[i][j] == '#':
      galaxies.append(dict({ 'x': j + (found_empty_cols * (EXP - 1)), 'y': i + (found_empty_rows * (EXP - 1)), 'id': cpt }))
      cpt += 1

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
