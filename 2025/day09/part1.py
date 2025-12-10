f = open('input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

largest_area = 0
for i, _ in enumerate(lines):
    for j, _ in enumerate(lines):
        if i == j:
            continue
        [x1, y1] = [int(s) for s in lines[i].split(',')]
        [x2, y2] = [int(s) for s in lines[j].split(',')]
        area = abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
        if area > largest_area:
            largest_area = area
print(largest_area)
