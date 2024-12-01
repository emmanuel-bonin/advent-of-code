import json

# f = open('./example1.txt')
# f = open('./example2.txt')
# f = open('./example3.txt')
f = open('./input.txt')

import sys
sys.setrecursionlimit(1000000)

lines = f.readlines()

PIPE_CHARS = '|-LJ7FS'

pipes = list()
j = 0
for l in lines:
  l = l.replace('\n', '').strip()
  for i in range(len(l)):
    if l[i] in PIPE_CHARS:
      pipes.append(dict({ 'pipe': l[i], 'x': i, 'y': j, 'visited': False, 'connected': list() }))
  j += 1

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

def find_connected_pipes(cur_pipe):
  for i in range(len(pipes)):
    pipe = pipes[i]
    if pipe['pipe'] == cur_pipe['pipe'] and pipe['x'] == cur_pipe['x'] and cur_pipe['y'] == pipe['y']:
      continue
    if is_connected(cur_pipe, pipe):
      if pipe['visited'] == False:
        cur_pipe['connected'].append(pipe)

def compute_connected(node):
  find_connected_pipes(node)
  node['visited'] = True
  for c in node['connected']:
    compute_connected(c)

def get_last_connected(cur_pipe, val=0):
  for c in cur_pipe['connected']:
    return get_last_connected(c, val+1)
  return val

start_end = [x for x in pipes if x['pipe'] == 'S'][0]
cur_pipe = start_end
compute_connected(cur_pipe)
print(json.dumps(cur_pipe, indent=2))

max_steps = get_last_connected(cur_pipe, 1)
print(max_steps / 2)
