f = open('input.txt', 'r')
lines = f.readlines()

def get_greater_num_idx(s):
    cur = 0
    res = 0
    i = 0
    while i < len(s):
        if int(s[i]) > cur:
            cur = int(s[i])
            res = i
        i += 1
    return res

res = 0
for line in lines:
    line = line.strip()
    idx_arr = []
    i = 0
    while i < 12:
        prev_idx = (idx_arr[len(idx_arr)-1] if len(idx_arr) > 0 else -1) + 1
        # Create a substring from previous found index (or 0 if first iteration) to length of line minus remaining numbers to find to reach 12
        # and get index of greater number in this string
        r = get_greater_num_idx(line[prev_idx:len(line)-(11-len(idx_arr))])
        idx_arr.append(r+prev_idx)
        i += 1
    res_s = ''
    # Create the number by concatenating numbers at each found indexes
    for i in idx_arr:
        res_s += line[i]
    res += int(res_s)

print(res)
