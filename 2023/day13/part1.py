# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')
# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')

lines = f.readlines()

patterns = []
current = []

for l in lines:
  l = l.replace('\n', '').strip()
  if l == '':
    patterns.append(current)
    current = []
  else:
    current.append(l)
patterns.append(current)

def get_pattern(p):
  res = ''
  i = 1
  for l in p:
    res += str(i) + '. ' + l + '\n'
    i += 1
  return res

def compute_horizontal_mirrors(p):
  print('is pattern horizontal mirror?')
  is_mirror = False
  for i in range(len(p) - 1):
    if p[i] == p[i + 1]:
      a = i
      b = i + 1
      is_mirror = True
      while a >= 0 and b < len(p):
        print('comparing lines', a+1, 'and', b+1, p[a], p[b])
        if p[a] != p[b]:
          print('diff between', a+1, b+1, p[a], p[b])
          is_mirror = False
          break
        a -= 1
        b += 1
    if is_mirror:
      print('pattern is horizontal between', i+1, i+2, 'with size', i+1)
      return i + 1
  print('pattern is not horizontal')
  return 0

def compute_vertical_mirrors(p):
  print('is pattern vertical mirror?')
  is_mirror = False
  for i in range(len(p[0]) - 1):
    if p[0][i] == p[0][i + 1]:
      is_mirror = True
      a = i
      b = i + 1
      while a >= 0 and b < len(p[0]):
        for l in range(len(p)):
          print('comparing char', a+1, 'and', b+1, 'at line', l+1, p[l][a], p[l][b])
          if p[l][a] != p[l][b]:
            print('diff between', a+1, b+1, 'at line', l+1, p[l][a], p[l][b])
            is_mirror = False
            break
        a -= 1
        b += 1
        if is_mirror == False:
          break
        else:
          if a < 0 or b >= len(p[0]):
            print(a < 0, b >= len(p[0]), len(p[0]))
            print('Found vertical mirror with a', a, 'and b', b, 'of size', i + 1)
            return i + 1
  if is_mirror == True:
    print('pattern is vertical between', i+1, i+2, 'with size', i+1)
    return i + 1
  print('pattern is not vertical')
  return 0

vert_mirr = []
hori_mirr = []
for p in patterns:
  print(get_pattern(p))
  vert_res = compute_vertical_mirrors(p)
  vert_mirr.append(vert_res)
  hori_res = compute_horizontal_mirrors(p)
  hori_mirr.append(hori_res)
  print('=========')

vert_res = 0
for v in vert_mirr:
  vert_res += v
hori_res = 0
for h in hori_mirr:
  hori_res += h * 100
print('vertical mirrors', vert_res)
print('horizontal mirrors', hori_res)

print('total', vert_res + hori_res)
