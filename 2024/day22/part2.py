import threading
import math
from functools import *

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


@lru_cache(maxsize=None)
def get_price_by_change_sequence(prices, changes, sequence):
    for i in range(len(changes) - 4):
        if changes[i:i + 4] == sequence:
            return prices[i + 4]


def extract_sequences(changes):
    seq = []
    for j in range(len(changes)):
        for i in range(len(changes[j]) - 4):
            seq.append(changes[j][i:i + 4])
    return seq


print('Computing secret numbers')

prices = []
price_idx = 0
for line in lines:
    line = line.strip('\n')
    secret = int(line)
    prices.append([])
    for i in range(2000):
        p = secret % 10
        prices[price_idx].append(p)
        r = compute(secret)
        secret = r
    price_idx += 1

print('Computed secret numbers\nComputing price and changes...')

changes = []
for i in range(len(prices)):
    changes.append([])
    for j in range(len(prices[i]) - 1):
        changes[i].append(prices[i][j + 1] - prices[i][j])

print('Computed price and changes\nComputing sequences by price...')

seq_by_price = {}
for n in range(9, -1, -1):
    if n not in seq_by_price:
        seq_by_price[n] = {}
    for i in range(len(prices)):
        if i not in seq_by_price[n]:
            seq_by_price[n][i] = []
        for j in range(len(prices[i]) - 4):
            if prices[i][j] == n and j > 5:
                seq_by_price[n][i].append(changes[i][j - 4:j - 1])

print('Computed sequences by price\nComputing best result...')

# print('Computed price and changes\nComputing sequences...')
# seq = extract_sequences(changes)
# print('Computed sequences\nComputing best result...')
#


# def run(_id, _seq, _prices, _changes):
#   result = 0
#   for s in range(len(_seq)):
#     current_res = 0
#     for i in range(len(_prices)):
#       r = get_price_by_change_sequence(tuple(_prices[i]), tuple(_changes[i]), tuple(_seq[s]))
#       if r is not None:
#         current_res += r
#     if current_res > result:
#       result = current_res
#       print('['+_id+'] Computed', s, 'out of', len(_seq), '(' + str(round((s / len(_seq)) * 100, 3)) + '%)', 'best sequence is', _seq[s], 'best result:', result)
#   print('['+_id+'] RESULT', result)
#
# run('main', seq, prices, changes)
#
# t1 = threading.Thread(target=run, args=('1', seq[0:len(seq)//8], prices, changes))
# t2 = threading.Thread(target=run, args=('2', seq[len(seq)//8:len(seq)//8*2], prices, changes))
# t3 = threading.Thread(target=run, args=('3', seq[len(seq)//8*2:len(seq)//8*3], prices, changes))
# t4 = threading.Thread(target=run, args=('4', seq[len(seq)//8*3:len(seq)//8*4], prices, changes))
# t5 = threading.Thread(target=run, args=('5', seq[len(seq)//8*4:len(seq)//8*5], prices, changes))
# t6 = threading.Thread(target=run, args=('6', seq[len(seq)//8*5:len(seq)//8*6], prices, changes))
# t7 = threading.Thread(target=run, args=('7', seq[len(seq)//8*6:len(seq)//8*7], prices, changes))
# t8 = threading.Thread(target=run, args=('8', seq[len(seq)//8*7:], prices, changes))
#
# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()
#
# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()
# t7.join()
# t8.join()
