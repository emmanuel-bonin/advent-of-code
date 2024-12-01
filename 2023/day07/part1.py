from functools import reduce, cmp_to_key

f = open("./input.txt", "r")
# f = open("./example.txt", "r")
lines = f.readlines()

CARD_VAL = '23456789TJQKA'
# 1. high card
# 2. one pair
# 3. two pairs
# 4. three of a kind
# 5. full
# 6. four of a kind
# 7. five of a kind

def is_five_of_a_kind(occurences):
  if len(occurences) == 1 and occurences[0]['n'] == 5:
    return True
  return False
def is_four_of_a_kind(occurences):
  if len(occurences) == 2 and (occurences[0]['n'] == 4 or occurences[1]['n'] == 4):
    return True
  return False
def is_full(occurences):
  found_3 = False
  found_2 = False
  for occ in occurences:
    if occ['n'] == 3:
      found_3 = True
    elif occ['n'] == 2:
      found_2 = True
  return found_2 == True and found_3 == True
def is_three_of_a_kind(occurences):
  found_3 = False
  for occ in occurences:
    if occ['n'] == 3:
      return True
  return False
def is_two_pairs(occurences):
  found_pair_1 = False
  for occ in occurences:
    if occ['n'] == 2:
      if found_pair_1 == False:
        found_pair_1 = True
      else:
        return True
  return False
def is_one_pair(occurences):
  for occ in occurences:
    if occ['n'] == 2:
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

final_list = list(reversed(fives + fours + fulls + threes + two_pairs + one_pairs + singles))
print(final_list)
result = 0
for i in range(len(final_list)):
  rank = i + 1
  result += final_list[i]['bid'] * rank
print(result)
