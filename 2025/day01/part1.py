input_file = open("./input.txt", "r")
lines = input_file.readlines()

dial_pos = 50
res = 0

for line in lines:
    n = int(line[1:])
    if n >= 100:
        n -= int(abs(n) / 100) * 100
    if line[0] == "L":
        dial_pos -= n
    elif line[0] == "R":
        dial_pos += n
    if dial_pos < 0:
        dial_pos += 100
    elif dial_pos > 99:
        dial_pos -= 100
    if dial_pos == 0:
        res += 1

print(res)
