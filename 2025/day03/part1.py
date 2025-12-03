f = open('input.txt', 'r')
lines = f.readlines()

def get_greater_num_idx(s, go_to_end=False, start_idx=-1):
    cur = 0
    res = 0
    max_idx = len(s) if go_to_end else len(s)-1
    i = 0 if start_idx == -1 else start_idx+1
    while i < max_idx:
        if int(s[i]) > cur:
            cur = int(s[i])
            res = i
        i += 1
    return res

res = 0
for line in lines:
    line = line.strip()
    idx1 = get_greater_num_idx(line, go_to_end=False)
    idx2 = get_greater_num_idx(line, go_to_end=True, start_idx=idx1)
    res += int(line[idx1]+line[idx2])

print(res)
