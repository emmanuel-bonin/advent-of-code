from functools import *

def parse(filename):
    data = []
    for l in open(filename).readlines():
        a, b = l.split(" ")
        data.append((a, tuple(map(int, b.split(",")))))
    return data

@lru_cache(maxsize=None)
# m = measurement ("#?.#"), s = survey (1,2,3), n = is next spot lava
def arr_cnt(m, s, n):
    # decreasing first value of tuple
    tr = lambda t: (t[0] - 1,) + t[1:]  # lru_cache demands tuples
    if not s:
        # no more number
        return 0 if "#" in m else 1
    elif not m:
        # no more spring group
        return 0 if sum(s) else 1
    elif s[0] == 0:
        # if current value in number of spring has reached 0 (after decreasing it with tr())
        return arr_cnt(m[1:], s[1:], False) if m[0] in ["?", "."] else 0
    elif n:
        # calling back function if next spot is # or ?
        return arr_cnt(m[1:], tr(s), True) if m[0] in ["?", "#"] else 0
    elif m[0] == "#":
        # calling back function is next spot is #
        return arr_cnt(m[1:], tr(s), True)
    elif m[0] == ".":
        # calling back function if next spot is .
        return arr_cnt(m[1:], s, False)
    else:
        # calling function back is next spot is ?
        return arr_cnt(m[1:], s, False) + arr_cnt(m[1:], tr(s), True)

data = parse("input.txt")

print(sum(arr_cnt(m, s, False) for m, s in data))

data2 = [(((m + "?") * 5)[:-1], s * 5) for m, s in data]

print(sum(arr_cnt(m, s, False) for m, s in data2))
