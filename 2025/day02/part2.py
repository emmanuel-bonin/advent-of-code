input_file = open("./input.txt", "r")
ranges_str = input_file.readlines()[0]
ranges = ranges_str[:-1].split(",")
input_file.close()

# Find for a given number, all the divisors of a number that result in an even number
# Uses a small cache system that prevents useless computing.
cached_divisors_by_len = {}
def find_divisors(n):
    global cached_divisors_by_len
    if n in cached_divisors_by_len:
        return cached_divisors_by_len[n]
    divisors = []
    i = 1
    while i <= n:
        if n % i == 0:
            divisors.append(i)
        i += 1
    cached_divisors_by_len[n] = divisors
    return divisors

# Compares first element in list with every other.
# Returns False if first element mismatches one of the other.
def all_elem_eq(arr):
    a = arr[0]
    i = 1
    while i < len(arr):
        if arr[i] != a:
            return False
        i += 1
    return True

# Smart split a string to certain lengths and checks the validity of an ID
def is_invalid(n):
    s = str(n)
    l = len(s)
    div = find_divisors(l)
    for d in div:
        if d == l:
            continue
        if all_elem_eq([''.join(s[x:x+d]) for x in range(0, len(s), d)]):
            return True
    return False

res = 0
for r in ranges:
    [min, max] = r.split("-")
    print("going from", min, "to", max)
    for i in range(int(min), int(max)+1):
        res += i if is_invalid(i) else 0
    print("res", res)
