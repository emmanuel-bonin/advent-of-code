from itertools import product

# f = open('./input.txt', 'r')
f = open('./example.txt', 'r')

lines = f.readlines()

def replace_rec(s, td):
  if '?' not in s:
    return [s]
  tmp_res = []
  for sub in [zip(td.keys(), chr) for chr in product(*td.values())]:
    tmp = s
    for repls in sub:
      tmp = tmp.replace(*repls, 1)
      tmp_res.append(replace_rec(tmp, td))
  return tmp_res

def flatten(l):
  if len(l) == 1:
    if type(l[0]) == list:
      result = flatten(l[0])
    else:
      result = l
  elif type(l[0]) == list:
    result = flatten(l[0]) + flatten(l[1:])
  else:
    result = [l[0]] + flatten(l[1:])
  return result

def is_valid(s, numbers):
  arr = s.split('.')
  arr = [x for x in arr if x != '']
  if len(arr) != len(numbers):
    return False
  for i in range(len(numbers)):
    if numbers[i] != len(arr[i]):
      return False
  return True

def compute_row(row):
  arr = row.split(' ')
  springs = arr[0]
  numbers = list(map(lambda x: int(x), arr[1].split(',')))
  n_unknown = len([x for x in springs if x == '?'])
  test_dict = {'?': ['.', '#']}
  possibilities_raw = replace_rec(springs, test_dict)
  possibilities = list(flatten(possibilities_raw))
  res = 0
  for i in range(len(possibilities)):
    if is_valid(possibilities[i], numbers):
      res += 1
  return res

res = 0
for l in lines:
  l = l.replace('\n', '').strip()
  res += compute_row(l)
print(res)
