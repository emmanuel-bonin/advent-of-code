from functools import *

f = open('input.txt', 'r')
lines = f.readlines()
f.close()

raw_patterns = lines[0].strip('\n').split(' ')
for i in range(len(raw_patterns)):
    raw_patterns[i] = raw_patterns[i].strip(',')
patterns = tuple(x for x in raw_patterns)
lines = lines[2:]
for i in range(len(lines)):
    lines[i] = lines[i].strip('\n')

cache = {}


@lru_cache(maxsize=None)
def match_pattern(patterns, line):
    result = 0
    if len(line) == 0:
        return 1
    else:
        for i in range(0, len(patterns)):
            if line.startswith(patterns[i]):
                result += match_pattern(patterns, line[len(patterns[i]):])
    return result


count = 0
for line in lines:
    s = match_pattern(patterns, line)
    if s > 0:
        count += s
print(count)
