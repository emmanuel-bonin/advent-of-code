# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')
f = open('./input.txt', 'r')

data = f.readlines()[0].strip().split(' ')


def trim_leading(num):
    res = num.lstrip('0')
    if res == '':
        return '0'
    return res


# Map containing the result computed for each number and times
cache = {}


def blink(n, times):
    if times == 0:
        return 1
    res = 1
    for i in range(times):
        if n == '0':
            n = '1'
        elif len(n) % 2 == 0:
            # Split the number in half and keeping the second one
            half = trim_leading(n[int(len(n) / 2):])
            # Set the first half in n for next iteration
            n = n[0:int(len(n) / 2)]

            # If the result for the half and times-(i+1) is already computed, use it
            if half in cache is not None and times - (i + 1) in cache[half] is not None:
                res += cache[half][times - (i + 1)]
            else:
                # Otherwise, compute it and store it in the cache
                a = blink(half, times - (i + 1))
                if half not in cache:
                    cache[half] = {}
                cache[half][times - (i + 1)] = a
                res += a
        else:
            n = str(int(n) * 2024)
    return res


N_BLINKS = 75
result = 0
for i in range(len(data)):
    a = blink(data[i], N_BLINKS)
    result += a

print(result)

f.close()
