from itertools import product
from functools import *
import re

f = open('./input.txt', 'r')
# f = open('./example.txt', 'r')

lines = f.readlines()

def transform_string(input_string):
  result = []
  current_group = input_string[0]
  for char in input_string[1:]:
    if char == current_group[-1]:
      current_group += char
    else:
      result.append(current_group)
      current_group = char
  result.append(current_group)
  return result

@cache
def replace_rec(s):
  td = {'?': ['.', '#']}
  if '?' not in s:
    return [s]
  tmp_res = []
  for sub in [zip(td.keys(), chr) for chr in product(*td.values())]:
    tmp = s
    for repls in sub:
      tmp = tmp.replace(*repls, 1)
      tmp_res.append(replace_rec(tmp))
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

@cache
def compute_possibilites(springs, numbers_str):
  numbers = list(map(lambda x: int(x), numbers_str.split(',')))
  res = 0
  possibilities_raw = replace_rec(springs)
  possibilities = list(flatten(possibilities_raw))
  matching = list()
  for i in range(len(possibilities)):
    if is_valid(possibilities[i], numbers):
      res += 1
      matching.append(possibilities[i])
  return res

def generate_combinations_with_existing_data(arr, replacements):
  result = [''.join(combination) for combination in product(*(replacements.get(char, [char]) for char in arr))]
  return result

group_alts = {}
for i in range(1, 15):
  k = ''
  for j in range(i):
    k += '?'
  group_alts[k] = flatten(replace_rec(k))

def compute_row(row):
  arr = row.split(' ')

  springs = arr[0]
  numbers_str = arr[1]
  numbers = list(map(lambda x: int(x), numbers_str.split(',')))
  print('transforming string')
  groups = transform_string(springs)
  print('generating alternatives')
  springs_alt = generate_combinations_with_existing_data(groups, group_alts)
  print('found', len(springs_alt), 'alternatives for', springs)

  res = 0
  for a in springs_alt:
    if is_valid(a, numbers):
      res += 1
      print('111', a, 'is valid for', numbers)
  res2 = 0

  # this loop is very slow
  for a in springs_alt:
    for b in springs_alt:
      aa = a + '.' + b
      ab = a + '#' + b
      if is_valid(aa, numbers + numbers):
        res2 += 1
        print('222', aa, 'is valid for', numbers + numbers)
      if is_valid(ab, numbers + numbers):
        res2 += 1
        print('333', ab, 'is valid for', numbers + numbers)

  result = int(res * pow(res2 / res, 4))
  return result

  # this is working correctly
  # res = compute_possibilites(springs, numbers_str)
  # print(res, 'possibilites for', springs)
  # res2 = compute_possibilites(springs + '?' + springs, numbers_str + ',' + numbers_str)
  # print(res2, 'possibilites for', springs + '?' + springs)
  # return int(res * pow(res2 / res, 4))

res = 0
i = 0
for l in lines:
  l = l.replace('\n', '').strip()
  res += compute_row(l)
  i += 1
  print('computed', i, 'lines')
print(res)
