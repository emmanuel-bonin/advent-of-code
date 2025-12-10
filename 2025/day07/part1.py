f = open('input.txt', 'r')
lines = [line.strip() for line in f.readlines()]
f.close()

rays_x = set()
res = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == 'S':
            rays_x.add(x)
            continue
        if lines[y][x] == '^':
            done = False
            while not done:
                done = True
                for rx in rays_x:
                    if rx == x:
                        res += 1
                        rays_x.add(x-1)
                        rays_x.add(x+1)
                        rays_x.remove(x)
                        break
print(res)
