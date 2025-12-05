f = open("input.txt", "r")
lines = [line.strip() for line in f.readlines()]

fresh_ids: list[tuple[int, int]] = []
ids: list[int] = []

transition = False
for line in lines:
    if line == "":
        transition = True
        continue
    if not transition:
        [min_id, max_id] = line.split("-")
        fresh_ids.append((int(min_id), int(max_id)))
    else:
        ids.append(int(line))

res = 0
for id in ids:
    for l in fresh_ids:
        if id >= l[0] and id <= l[1]:
            res += 1
            break
print(res)
