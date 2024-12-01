f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

line = f.readlines()[0]

strs = line.split(',')

def run_hash(s):
  current = 0
  for c in s:
    current += ord(c)
    current *= 17
    current %= 256
  return current

res = 0
boxes = []
for i in range(256):
  boxes.append({
    'number': i + 1,
    'lenses': []
  })

def remove_lens(box, label):
  for i in range(len(box['lenses'])):
    l = box['lenses'][i]
    if l['label'] == label:
      del box['lenses'][i]
      box['lenses'] = list(filter(lambda b: b is not None, box['lenses']))
      break

def add_lens(box, label, focal):
  found = False
  for i in range(len(box['lenses'])):
    l = box['lenses'][i]
    if l['label'] == label:
      l['focal'] = focal
      found = True
      break
  if found == False:
    box['lenses'].append({ 'label': label, 'focal': focal })

def print_boxes(boxes):
  for b in boxes:
    print('Box', b['number'])
    for l in b['lenses']:
      print(l)

for s in strs:
  s = s.replace('\n', '').strip()
  sep = '=' if '=' in s else '-'
  label = s.split(sep)[0]
  box_idx = run_hash(label)
  if sep == '-':
    remove_lens(boxes[box_idx], label)
  else:
    focal = -1 if '-' in s else s.split('=')[1]
    add_lens(boxes[box_idx], label, int(focal))

res = 0
for b in boxes:
  for i in range(len(b['lenses'])):
    res += b['number'] * (i + 1) * b['lenses'][i]['focal']
print(res)
