f = open('input.txt', 'r')
lines = f.readlines()
f.close()

patterns = lines[0].strip('\n').split(' ')
for i in range(len(patterns)):
    patterns[i] = patterns[i].strip(',')
lines = lines[2:]
for i in range(len(lines)):
    lines[i] = lines[i].strip('\n')

cache = {}


def match_pattern(patterns, line):
    if len(line) == 0:
        return True
    else:
        for i in range(0, len(patterns)):
            if line.startswith(patterns[i]):
                if patterns[i] in cache:
                    if line[len(patterns[i]):] in cache[patterns[i]]:
                        return cache[patterns[i]][line[len(patterns[i]):]]
                if match_pattern(patterns, line[len(patterns[i]):]):
                    if not patterns[i] in cache:
                        cache[patterns[i]] = {}
                    cache[patterns[i]] = {line[len(patterns[i]):]: True}
                    return True
                else:
                    if not patterns[i] in cache:
                        cache[patterns[i]] = {}
                    cache[patterns[i]] = {line[len(patterns[i]):]: False}
        return False


count = 0
for line in lines:
    if match_pattern(patterns, line):
        count += 1
print(count)
