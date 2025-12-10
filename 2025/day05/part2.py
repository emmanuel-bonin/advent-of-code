f = open("input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

ranges: list[list[int]] = []

for line in lines:
    if line == "":
        break
    [start, end] = line.split("-")
    ranges.append([int(start), int(end)])

finished = False
while not finished:
    finished = True
    i = 0
    while i < len(ranges):
        j = 0
        while j < len(ranges):
            if j == i:
                j += 1
                continue
            # if current range in contained in second range, we remove it
            if ranges[i][0] >= ranges[j][0] and ranges[i][1] <= ranges[j][1]:
                ranges.pop(i)
                finished = False
                j += 1
                break
            # if current range overlaps second range by the end, we merge them
            elif ranges[i][0] >= ranges[j][0] and ranges[i][1] > ranges[j][1] and ranges[i][1] <= ranges[j][0]:
                ranges[j][1] = ranges[i][1]
                ranges.pop(i)
                finished = False
                j += 1
                break
            # if current range overlaps second range by the start, we merge them
            elif ranges[i][0] < ranges[j][0] and ranges[i][1] <= ranges[j][1] and ranges[i][1] >= ranges[j][0]:
                ranges[j][0] = ranges[i][0]
                ranges.pop(i)
                finished = False
                j += 1
                break
            j += 1
        i += 1

print(ranges)

res = 0
for r in ranges:
    res += r[1] - r[0] + 1

print(res)
