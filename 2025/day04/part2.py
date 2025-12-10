f = open("input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

def count_nearby_rolls(_lines: list[str], _x: int, _y: int):
    max_x = len(_lines[0])-1
    max_y = len(_lines)-1
    return (
        (0 if _y-1 < 0 or _x-1 < 0 else 1 if _lines[_y-1][_x-1] == '@' else 0) +
        (0 if _y-1 < 0 else 1 if _lines[_y-1][_x] == '@' else 0) +
        (0 if _y-1 < 0 or _x+1 > max_x else 1 if _lines[_y-1][_x+1] == '@' else 0) +
        (0 if _x-1 < 0 else 1 if _lines[_y][_x-1] == '@' else 0) +
        (0 if _x+1 > max_x else 1 if _lines[_y][_x+1] == '@' else 0) +
        (0 if _y+1 > max_y or _x-1 < 0 else 1 if _lines[_y+1][_x-1] == '@' else 0) +
        (0 if _y+1 > max_y else 1 if _lines[_y+1][_x] == '@' else 0) +
        (0 if _y+1 > max_y or _x+1 > max_x else 1 if _lines[_y+1][_x+1] == '@' else 0)
    )

res = 0
finished = False
while not finished:
    finished = True
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "@":
                adj_rolls = count_nearby_rolls(lines, x, y)
                if adj_rolls < 4:
                    lines[y] = lines[y][:x] + '.' + lines[y][x+1:]
                    res += 1
                    finished = False

print(res)
