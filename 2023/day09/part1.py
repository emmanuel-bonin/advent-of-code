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
  data[len(data) - 1].append(0)
  i = len(data) - 2
  while i >= 0:
    prev_data = data[i + 1][len(data[i + 1]) - 1]
    cur_data = data[i][len(data[i]) - 1]
    data[i].append(prev_data + cur_data)
    i -= 1
  return data

res = 0
for l in lines:
  l = l.replace('\n', '')
  data = l.split(' ')
  diff = generate_diff(list(map(lambda x: int(x), data)))
  diff = predicate(diff)
  res += diff[0][len(diff[0]) - 1]
print(res)
