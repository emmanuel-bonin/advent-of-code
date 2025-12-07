import math

f = open("input.txt", "r")
lines = [line.replace('\n', '') for line in f.readlines()]

def compute_indexes(s):
    i = 0
    start = -1
    end = -1
    while i < len(s):
        if s[i] >= '0' and s[i] <= '9':
            if start == -1:
                start = i
            while i < len(s) and s[i] >= '0' and s[i] <= '9':
                i += 1
            if end == -1:
                end = i
            break
        elif s[i] == ' ':
            while i < len(s) and s[i] == ' ':
                i += 1
    return [start, end]

def get_wider_interval(arr):
    wider = []
    for elem in arr:
        if wider == [] or wider[1] - wider[0] < elem[1]-elem[0]:
            wider = elem
    return wider

def count_spaces(s):
    cpt = 0
    for elem in s:
        if elem[0] == ' ':
            cpt += 1
    return cpt

operators = lines.pop().split(' ')
finished = False
while not finished:
    finished = True
    for op in operators:
        if op == '':
            finished = False
            operators.remove(op)
            break

numbers = []
finished = False
while not finished:
    i = 0
    finished = True
    indexes = []
    cur_nums = []
    while i < len(lines):
        number_indexes = compute_indexes(lines[i])
        if number_indexes[0] == number_indexes[1]:
            break
        else:
            finished = False
        indexes.append(number_indexes)
        i += 1
    if len(indexes) == 0:
        break
    wider = get_wider_interval(indexes)
    i = 0
    while i < len(lines):
        cur_nums.append(lines[i][wider[0]:wider[1]])
        lines[i] = lines[i][:wider[0]] + lines[i][wider[1]:]
        i += 1
    numbers.append(cur_nums)

res = 0
k = len(operators)-1
while k >= 0:
    operands = numbers[k][::-1]
    cur_res = 0
    while len(operands[0]) > 0:
        i = len(operands) - 1
        n = 0
        while i >= 0:
            p = count_spaces(operands[:i])
            n = n + (int(math.pow(10, i-p)) * int(operands[i][0] if operands[i][0] != ' ' else '0'))
            operands[i] = operands[i][1:]
            i-=1
        if cur_res == 0:
            cur_res = n
        else:
            if operators[k] == '+':
                cur_res += n
            else:
                cur_res *= n
    res += cur_res
    k -= 1

print(res)

# 123 328 .51 64.
# .45 64. 387 23.
# ..6 98. 215 314
# *   +   *   +
