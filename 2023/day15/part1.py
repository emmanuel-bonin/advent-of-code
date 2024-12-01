# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

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
for s in strs:
  s = s.replace('\n', '').strip()
  h = run_hash(s)
  res += h
  print('for string', s, 'value is', h)
print(res)
