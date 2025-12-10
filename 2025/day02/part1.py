input_file = open("./input.txt", "r")
ranges_str = input_file.readlines()[0]
ranges = ranges_str[:-1].split(",")
input_file.close()

def is_invalid(n):
    s = str(n)
    first, second = s[:len(s)//2], s[len(s)//2:]
    return first == second

res = 0
for r in ranges:
    [min, max] = r.split("-")
    print("going from", min, "to", max)
    for i in range(int(min), int(max)+1):
        if is_invalid(i):
            res += i
    print("res", res)
