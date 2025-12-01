input_file = open("./input.txt", "r")
lines = input_file.readlines()

dial_pos = 50
res = 0

for line in lines:
    n = int(line[1:])
    if n >= 100:
        n %= 100
    if line[0] == "L":
        dial_pos = dial_pos - n + 100 if dial_pos - n < 0 else dial_pos - n
    elif line[0] == "R":
        dial_pos = dial_pos + n - 100 if dial_pos + n > 99 else dial_pos + n
    if dial_pos == 0:
        res += 1

print(res)
