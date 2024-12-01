f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')
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
  for l in p:
    res += l + '\n'
  return res

def compute_horizontal_mirrors(p, prev):
  is_mirror = False
  for i in range(len(p) - 1):
    if p[i] == p[i + 1]:
      a = i
      b = i + 1
      is_mirror = True
      while a >= 0 and b < len(p):
        if p[a] != p[b]:
          is_mirror = False
          break
        a -= 1
        b += 1
    if is_mirror and i + 1 != prev:
      return i + 1
    else:
      is_mirror = False
  return 0

def compute_vertical_mirrors(p, prev):
  is_mirror = False
  for i in range(len(p[0]) - 1):
    if p[0][i] == p[0][i + 1]:
      is_mirror = True
      a = i
      b = i + 1
      while a >= 0 and b < len(p[0]):
        for l in range(len(p)):
          if p[l][a] != p[l][b]:
            is_mirror = False
            break
        a -= 1
        b += 1
        if is_mirror == False:
          break
        else:
          if a < 0 or b >= len(p[0]):
            if i + 1 == prev:
              is_mirror = False
            else:
              return i + 1
  return i + 1 if is_mirror == True else 0

vert_mirr = []
hori_mirr = []
for pat in patterns:
  p = pat.copy()

  vert_res = compute_vertical_mirrors(pat, 0)
  hori_res = compute_horizontal_mirrors(pat, 0)

  nb_lines = len(p)
  nb_char = len(p[0])
  nb_new_patterns = nb_lines * nb_char

  pat_vert_res = []
  pat_hori_res = []
  for l in range(nb_lines):
    for c in range(nb_char):
      p = pat.copy()
      if p[l][c] == '#':
        li = list(p[l])
        li[c] = '.'
        p[l] = ''.join(li)
      else:
        li = list(p[l])
        li[c] = '#'
        p[l] = ''.join(li)
      vert_res2 = compute_vertical_mirrors(p, vert_res)
      hori_res2 = compute_horizontal_mirrors(p, hori_res)
      if vert_res2 and vert_res2 != vert_res:
        pat_vert_res.append(vert_res2)
      if hori_res2 and hori_res2 != hori_res:
        pat_hori_res.append(hori_res2)

  print('horizontal old result', hori_res)
  print('horizontal new result', pat_hori_res[0] if len(pat_hori_res) else 0)
  if len(pat_hori_res):
    hori_mirr.append(pat_hori_res[0])

  print('vertical old result', vert_res)
  print('vertical new result', pat_vert_res[0] if len(pat_vert_res) else 0)
  if len(pat_vert_res):
    vert_mirr.append(pat_vert_res[0])

  print('=========')

vert_res = 0
for v in vert_mirr:
  vert_res += v
hori_res = 0
for h in hori_mirr:
  hori_res += h * 100

print('total', vert_res + hori_res)
