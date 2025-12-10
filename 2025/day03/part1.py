f = open('input.txt', 'r')
lines = f.readlines()
f.close()

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
    idx1 = get_greater_num_idx(line[:len(line)-1])
    idx2 = get_greater_num_idx(line[idx1+1:]) + idx1+1
    res += int(line[idx1]+line[idx2])

print(res)
