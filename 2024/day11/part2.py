# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')
f = open('./input.txt', 'r')

data = f.readlines()[0].strip().split(' ')

def trim_leading(num):
  res = num.lstrip('0')
  if res == '':
    return '0'
  return res

# Map containing the result computed for each number and times
map = {}

def blink(n, times):
  if times == 0:
    return 1
  res = 1
  for i in range(times):
    if n == '0':
      n = '1'
    elif len(n) % 2 == 0:
      h1 = n[0:int(len(n)/2)]
      h2 = trim_leading(n[int(len(n)/2):])
      n = h1
      if h2 in map is not None and times-(i+1) in map[h2] is not None:
        res += map[h2][times-(i+1)]
      else:
        a = blink(h2, times-(i+1))
        if h2 not in map:
          map[h2] = {}
        map[h2][times-(i+1)] = a
        res += a
    else:
      n = str(int(n) * 2024)
  return res

# Precompute all the numbers from 0 to 999 with 20 blinks
for i in range(1000):
  for j in range(20):
    a = blink(str(i), j)
    if str(i) not in map:
      map[str(i)] = {}
    map[str(i)][j] = a

N_BLINKS = 75
result = 0
for i in range(len(data)):
  a = blink(data[i], N_BLINKS)
  result += a

print(result)

f.close()
