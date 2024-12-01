import json
from shapely.geometry import Point, Polygon

# f = open('./example1.txt')
# f = open('./example2.txt')
# f = open('./example3.txt')
# f = open('./example6.txt')
f = open('./input.txt')

lines = f.readlines()

PIPE_CHARS = '|-LJ7FS'

pipes = list()
cases = list()
j = 0
print('Generating lines...')
for l in lines:
  l = l.replace('\n', '').strip()
  for i in range(len(l)):
    if l[i] == '.':
      cases.append(Point(i, j))
    elif l[i] in PIPE_CHARS:
      pipes.append(dict({ 'pipe': l[i], 'x': i, 'y': j }))
  j += 1
print('Done generating lines')

def is_connected(cur_pipe, pipe):
  if pipe['pipe'] == '-':
    if pipe['y'] == cur_pipe['y']:
      if pipe['x'] == cur_pipe['x'] - 1:
        return cur_pipe['pipe'] not in '|LF'
      elif pipe['x'] == cur_pipe['x'] + 1:
        return cur_pipe['pipe'] not in '|J7'
    return False
  elif pipe['pipe'] == '|':
    if pipe['x'] == cur_pipe['x']:
      if pipe['y'] == cur_pipe['y'] - 1:
        return cur_pipe['pipe'] not in '-7F'
      if pipe['y'] == cur_pipe['y'] + 1:
        return cur_pipe['pipe'] not in '-JL'
    return False
  elif pipe['pipe'] == 'L':
    if pipe['x'] == cur_pipe['x'] - 1 and pipe['y'] == cur_pipe['y']:
      return cur_pipe['pipe'] not in '|LF'
    elif pipe['x'] == cur_pipe['x'] and pipe['y'] == cur_pipe['y'] + 1:
      return cur_pipe['pipe'] not in '-LJ'
    return False
  elif pipe['pipe'] == 'J':
    if pipe['x'] == cur_pipe['x'] + 1 and pipe['y'] == cur_pipe['y']:
      return cur_pipe['pipe'] not in '|7J'
    elif pipe['x'] == cur_pipe['x'] and pipe['y'] == cur_pipe['y'] + 1:
      return cur_pipe['pipe'] not in '-JL'
    return False
  elif pipe['pipe'] == '7':
    if pipe['x'] == cur_pipe['x'] + 1 and pipe['y'] == cur_pipe['y']:
      return cur_pipe['pipe'] not in '|J7'
    elif pipe['x'] == cur_pipe['x'] and pipe['y'] == cur_pipe['y'] - 1:
      return cur_pipe['pipe'] not in '-F7'
    return False
  elif pipe['pipe'] == 'F':
    if pipe['x'] == cur_pipe['x'] - 1 and pipe['y'] == cur_pipe['y']:
      return cur_pipe['pipe'] not in '|FL'
    elif pipe['x'] == cur_pipe['x'] and pipe['y'] == cur_pipe['y'] - 1:
      return cur_pipe['pipe'] not in '-F7'

print('Finding start point...')
start_end = [x for x in pipes if x['pipe'] == 'S'][0]
print('Done finding start point')
pipes.remove(start_end)
cur_pipe = start_end

starts = list()
print('Finding node at right of start...')
start_right_list = [x for x in pipes if x['x'] == cur_pipe['x'] + 1 and x['y'] == cur_pipe['y']]
if len(start_right_list):
  starts.append(start_right_list[0])
print('Done finding node at right of start')

print('Finding node at bottom of start...')
start_bot_list = [x for x in pipes if x['x'] == cur_pipe['x'] and x['y'] == cur_pipe['y'] + 1]
if len(start_bot_list):
  starts.append(start_bot_list[0])
print('Done finding node at bottom of start')

print('Finding node at left of start...')
start_left_list = [x for x in pipes if x['x'] == cur_pipe['x'] - 1 and x['y'] == cur_pipe['y']]
if len(start_left_list):
  starts.append(start_left_list[0])
print('Done finding node at left of start')

print('Finding node at top of start...')
start_top_list = [x for x in pipes if x['x'] == cur_pipe['x'] and x['y'] == cur_pipe['y'] - 1]
if len(start_top_list):
  starts.append(start_top_list[0])
print('Done finding node at top of start')

print('Removing non connected nodes next to start...')
finished = False
while finished == False:
  finished = True
  for i in range(len(starts)):
    if not is_connected(start_end, starts[i]):
      del starts[i]
      finished = False
      break
print('Done removing non connected nodes next to start')

print('Filtering pipes to delete start of main loop...')
corners = list()
start = starts[0]
for i in range(len(pipes)):
  if pipes[i]['x'] == start['x'] and pipes[i]['y'] == start['y']:
    del pipes[i]
    break
print('Done filtering pipes to delete start of main loop...')

end = starts[1]
corners.append(Point(start_end['x'], start_end['y']))
print('Finding each corners of main loop...')
while start != end:
  for i in range(len(pipes)):
    pipe = pipes[i]
    if is_connected(start, pipe):
      if pipe['pipe'] in 'FJ7L':
        corners.append(Point(pipe['x'], pipe['y']))
      start = pipe
      del pipes[i]
      break
print('Done finding each corners of main loop...')

# Adding non-connected pipes to cases to compute
for pipe in pipes:
  cases.append(Point(pipe['x'], pipe['y']))

print('Checking if cases in polygon...')
poly = Polygon(corners)
res = 0
for c in cases:
  if poly.contains(c):
    res += 1
print('Done checking if cases in polygon...')

print(res)
