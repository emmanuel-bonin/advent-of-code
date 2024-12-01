f = open('./input.txt', 'r')
# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')

lines = f.readlines()

nodes = dict()
instructions = lines[0].replace('\n', '').strip()
cur_node = 'AAA'
for l in lines[2:]:
  l = l.replace('\n', '')
  arr = l.split('=')
  if len(arr) > 0:
    children = arr[1].split(',')
    arr[0] = arr[0].strip()
    children[0] = children[0].replace('(', '').strip()
    children[1] = children[1].replace(')', '').strip()
    nodes[arr[0]] = dict({ 'L': children[0], 'R': children[1] })

step = 0
found = False
while cur_node != 'ZZZ':
  for i in instructions:
    cur_node = nodes[cur_node][i]
    step += 1
    if cur_node == 'ZZZ':
      found = True
      break
  if found == True:
    break
print(step)
