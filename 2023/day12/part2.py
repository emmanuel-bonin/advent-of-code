from functools import *

f = open('./example1.txt', 'r')
# f = open('./example.txt', 'r')
# f = open('./input.txt', 'r')
lines = f.readlines()

@lru_cache(maxsize=None)
def count(spring, group):
  if len(group) == 0:
    print('##### RETURNING 1 for', spring, group)
    return 1
  elif len(spring) == 0:
    print('111111 RETURNING 0 for', spring, group)
    return 0
  if spring[0] == '#':
    if spring.startswith('#' * group[0]):
      if group[0] > 1:
        print('matched', spring, group, '=> counting for', spring[group[0]:], group[1:])
        return count(spring[group[0]:], group[1:])
      else:
        print('matched', spring, group, '=> counting for', spring[1:], group[1:])
        return count(spring[1:], group[1:])
    else:
      print('222222 RETURNING 0 for', spring, group)
      return 0
  elif spring[0] == '?':
    print('on ? counting for both configurations')
    print('=====>', '#' + spring[1:], (group[0]-1, *group[1:]))
    print('=====>', '.' + spring[1:], group)
    c1 = count('#' + spring[1:], (group[0]-1, *group[1:]))
    c2 = count('.' + spring[1:], group)
    return c1 + c2
  elif spring[0] == '.':
    print('ignoring . => counting for', spring[1:], group)
    return count(spring[1:], group)
  print('33333333 RETURNING 0 for', spring, group)
  return 0

data = []
for l in lines:
  springs, groups = l.split(' ')
  data.append((springs, tuple(map(int, groups.split(',')))))
#   data.append((springs*5, tuple(map(int, groups.split(',')))*5))

res = 0
for spring, group in data:
  tmp = count(spring, group)
  print('for', spring, group, ' => ', tmp)
  res += tmp

print(res)
