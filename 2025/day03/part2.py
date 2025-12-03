f = open('input.txt', 'r')
lines = f.readlines()

def get_greater_num_idx(s, start=-1, margin_end=-1):
    cur = 0
    res = 0
    max_idx = len(s) if margin_end == -1 else len(s)-margin_end
    i = start + 1
    while i <= max_idx:
        if int(s[i]) > cur:
            cur = int(s[i])
            res = i
        i += 1
    return res

res = 0
for line in lines:
    line = line.strip()
    idx_arr = []
    for i in range(12):
        r = get_greater_num_idx(line, start=idx_arr[len(idx_arr)-1] if len(idx_arr) > 0 else -1, margin_end=12-len(idx_arr))
        idx_arr.append(r)
    res_s = ''
    for i in idx_arr:
        res_s += line[i]
    res += int(res_s)

print(res)
