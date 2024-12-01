f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

def generate_diff(data):
  res = list()
  res.append(data)
  all_zero = False
  while all_zero == False:
    diff = list()
    for i in range(len(data) - 1):
      diff.append(data[i + 1] - data[i])
      i += 1
    all_zero = True
    for i in diff:
      if i != 0:
        all_zero = False
        break
    res.append(diff)
    data = diff
  return res

def predicate(data):
  print('before', data)
  data[len(data) - 1].insert(0, 0)
  i = len(data) - 2
  while i >= 0:
    prev_data = data[i + 1][0]
    cur_data = data[i][0]
    data[i].insert(0, cur_data - prev_data)
    i -= 1
  print('after', data)
  return data

res = 0
for l in lines:
  l = l.replace('\n', '')
  data = l.split(' ')
  diff = generate_diff(list(map(lambda x: int(x), data)))
  diff = predicate(diff)
  res += diff[0][0]
print(res)
