from functools import *

f = open('./input.txt', 'r')
lines = f.readlines()

data = []
for l in lines:
  springs, groups = l.split(' ')
  data.append((springs, tuple(map(int, groups.split(',')))))

@lru_cache(maxsize=None)
def count(spring, group, is_broken):
  # if no more member un group, return 0 if a # is still in spring else 1

  # if no more spring, return 0 sum(group) returns something (no more # but still groups to find) else 1

  # if the first value of group is 0 (reached after decreasing), call back function with spring and group shifted by 1 elem, if current spring is ? or .

  # if is_broken is true, call back function with shifted
  pass

res = sum(count(spring, group) for spring, group in data)
