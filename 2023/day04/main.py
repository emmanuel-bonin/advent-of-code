import re
import json

f = open("./input.txt", "r")
# f = open("./example.txt", "r")
lines = f.readlines()

cards = dict()
result = 0
n = 0
for l in lines:
    l = l.replace('\n', '')
    numbers = re.findall(r'\S+', l)
    # winning = numbers[2:7]
    # yours = numbers[8::]
    winning = numbers[2:12]
    yours = numbers[13::]
    cards[str(n)] = dict({ 'winning': winning, 'yours': yours, 'n': 1 })
    n += 1

i = 0
for x in cards:
    c = cards[str(x)]
    matches = 0
    for a in c['winning']:
        for b in c['yours']:
            if a == b:
                matches += 1
    j = i + 1
    while j < i + matches + 1 and j < len(cards):
        cards[str(j)]['n'] += 1 * c['n']
        j += 1
    i += 1

for x in cards:
    result += cards[x]['n']
print(result)
