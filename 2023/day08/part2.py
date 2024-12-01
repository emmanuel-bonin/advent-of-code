f = open('./input.txt', 'r')
# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')
# f = open('./example3.txt', 'r')

lines = f.readlines()

nodes = dict()
instructions = lines[0].replace('\n', '').strip()
cur_nodes = list()
for l in lines[2:]:
  l = l.replace('\n', '')
  arr = l.split('=')
  if len(arr) > 0:
    children = arr[1].split(',')
    arr[0] = arr[0].strip()
    children[0] = children[0].replace('(', '').strip()
    children[1] = children[1].replace(')', '').strip()
    nodes[arr[0]] = dict({ 'L': children[0], 'R': children[1] })
    if arr[0].endswith('A'):
      cur_nodes.append(arr[0])

def go_to_node(start, end):
  step = 0
  found = False
  cur_node = start
  while found == False:
    for i in instructions:
      cur_node = nodes[cur_node][i]
      step += 1
      if cur_node == end:
        found = True
        break
    if found == True:
      break
  return step

def gcd(a, b):
  if b == 0:
    return a
  return gcd(b, a % b)

def lcm(a, b):
  if a > b:
    return (a / gcd(a, b)) * b
  else:
    return (b / gcd(a, b)) * a

step1 = go_to_node('AAA', 'ZZZ')
step2 = go_to_node('DVA', 'XDZ')
step3 = go_to_node('VXA', 'TNZ')
step4 = go_to_node('JHA', 'FRZ')
step5 = go_to_node('NMA', 'JFZ')
step6 = go_to_node('PXA', 'LHZ')

lcm1 = lcm(step1, step2)
lcm2 = lcm(step3, step4)
lcm3 = lcm(step5, step6)
lcm4 = lcm(lcm1, lcm2)

total_steps = lcm(lcm3, lcm4)

# total_steps = find_lcm([step1, step2, step3, step4, step5, step6])
print(total_steps)
