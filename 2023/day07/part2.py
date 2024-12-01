from functools import reduce, cmp_to_key

f = open("./input.txt", "r")
# f = open("./example.txt", "r")
lines = f.readlines()

CARD_VAL = 'J23456789TQKA'

def is_five_of_a_kind(occurences):
  if len(occurences) == 1 and occurences[0]['n'] == 5:
    return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker > 0 and len(occurences) == 2:
    return True
  return False

def is_four_of_a_kind(occurences):
  occurences = sorted(occurences, key=lambda x: x['n'], reverse=True)
  if len(occurences) == 2 and (occurences[0]['n'] == 4 or occurences[1]['n'] == 4):
    return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker == 1:
    return occurences[0]['n'] == 3 and occurences[1]['n'] == 1 and occurences[2]['n'] == 1
  elif n_joker == 2:
    return occurences[0]['n'] == 2 and occurences[1]['n'] == 2 and occurences[2]['n'] == 1
  return False

def is_full(occurences):
  occurences = sorted(occurences, key=lambda x: x['n'], reverse=True)
  found_3 = False
  found_2 = False
  for occ in occurences:
    if occ['n'] == 3:
      found_3 = True
    elif occ['n'] == 2:
      found_2 = True
  if found_2 == True and found_3 == True:
    return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker > 0 and len(occurences) == 3:
    return True
  return False

def is_three_of_a_kind(occurences):
  occurences = sorted(occurences, key=lambda x: x['n'], reverse=True)
  found_3 = False
  for occ in occurences:
    if occ['n'] == 3:
      return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker > 0 and len(occurences) == 4:
    return True
  return False

def is_two_pairs(occurences):
  occurences = sorted(occurences, key=lambda x: x['n'], reverse=True)
  found_pair_1 = False
  for occ in occurences:
    if occ['n'] == 2:
      if found_pair_1 == False:
        found_pair_1 = True
      else:
        return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker > 0 and len(occurences) == 4:
    return True
  return False

def is_one_pair(occurences):
  occurences = sorted(occurences, key=lambda x: x['n'], reverse=True)
  for occ in occurences:
    if occ['n'] == 2:
      return True
  n_joker = reduce(lambda acc, c: acc + c['n'] if c['char'] == 'J' else acc, occurences, 0)
  if n_joker > 0:
    return True
  return False

def compare_max_card(card1, card2):
  s1 = card1['hand']
  s2 = card2['hand']
  i = 0
  while i < len(s1):
    c1 = CARD_VAL.find(s1[i])
    c2 = CARD_VAL.find(s2[i])
    if c1 < c2:
      return -1
    elif c2 < c1:
      return 1
    i += 1
  return 0

fives = list()
fours = list()
fulls = list()
threes = list()
two_pairs = list()
one_pairs = list()
singles = list()
for l in lines:
  l = l.replace('\n', '')
  if l == '':
    continue
  arr = l.split(' ')

  card = dict({ 'hand': arr[0], 'bid': int(arr[1]) })
  occurences = list()
  for j in range(len(CARD_VAL)):
    char_to_count = CARD_VAL[j]
    count = reduce(lambda acc, c: acc + 1 if c == char_to_count else acc, card['hand'], 0)
    if count > 0:
      occurences.append(dict({ 'char': CARD_VAL[j], 'n': count }))
  if is_five_of_a_kind(occurences):
    fives.append(card)
  elif is_four_of_a_kind(occurences):
    fours.append(card)
  elif is_full(occurences):
    fulls.append(card)
  elif is_three_of_a_kind(occurences):
    threes.append(card)
  elif is_two_pairs(occurences):
    two_pairs.append(card)
  elif is_one_pair(occurences):
    one_pairs.append(card)
  else:
    singles.append(card)

fives = sorted(fives, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
fours = sorted(fours, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
fulls = sorted(fulls, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
threes = sorted(threes, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
two_pairs = sorted(two_pairs, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
one_pairs = sorted(one_pairs, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)
singles = sorted(singles, key=cmp_to_key(lambda c1, c2: compare_max_card(c1, c2)), reverse=True)

print('fives =====>', fives)
print('fours =====>', fours)
print('fulls =====>', fulls)
print('threes =====>', threes)
print('two_pairs =====>', two_pairs)
print('one_pairs =====>', one_pairs)
print('singles =====>', singles)

final_list = list(reversed(fives + fours + fulls + threes + two_pairs + one_pairs + singles))
# print(final_list)
result = 0
for i in range(len(final_list)):
  rank = i + 1
  result += final_list[i]['bid'] * rank
print(result)
