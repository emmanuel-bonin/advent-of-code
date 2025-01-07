import math

f = open('input.txt', 'r')
lines = f.readlines()
f.close()


def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def compute(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(math.floor(secret / 32), secret))
    return prune(mix(secret * 2048, secret))


result = 0
for line in lines:
    line = line.strip('\n')
    secret = int(line)
    for i in range(2000):
        r = compute(secret)
        secret = r
    result += secret
print(result)
