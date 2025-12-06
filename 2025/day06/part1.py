f = open("input.txt", "r")
lines = [line.strip() for line in f.readlines()]

ops = []
for line in lines:
    ops_dirty = line.split(' ')
    finished = False
    while not finished:
        finished = True
        for op in ops_dirty:
            if op == '':
                ops_dirty.remove(op)
                finished = False
                break
    ops.append(ops_dirty)

res = 0
i = 0
while i < len(ops[0]):
    j = 0
    unary_op = []
    while j < len(ops):
        unary_op.append(ops[j][i])
        j += 1
    cur_res = 0
    operator = unary_op.pop()
    for n in unary_op:
        if operator == '+':
            cur_res += int(n)
        elif operator == '*':
            if cur_res == 0:
                cur_res = int(n)
            else:
                cur_res *= int(n)
    res += cur_res
    i += 1
print(res)
