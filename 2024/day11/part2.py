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
      half = trim_leading(n[int(len(n)/2):])
      n = n[0:int(len(n)/2)]
      if half in map is not None and times-(i+1) in map[half] is not None:
        res += map[half][times-(i+1)]
      else:
        a = blink(half, times-(i+1))
        if half not in map:
          map[half] = {}
        map[half][times-(i+1)] = a
        res += a
    else:
      n = str(int(n) * 2024)
  return res

N_BLINKS = 75
result = 0
for i in range(len(data)):
  a = blink(data[i], N_BLINKS)
  result += a

print(result)

f.close()
