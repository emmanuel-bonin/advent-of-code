# f = open('./example1.txt', 'r')
# f = open('./example2.txt', 'r')
f = open('./input.txt', 'r')

data = f.readlines()[0].strip().split(' ')

def trim_leading(num):
  res = num.lstrip('0')
  if res == '':
    return '0'
  return res

def blink(num):
  res = []
  for i in range(len(num)):
    length = int(len(num[i]))

    if num[i] == '0':
      res.append('1')
    elif length % 2 == 0:
      res.append(trim_leading(num[i][0:int(length/2)]))
      res.append(trim_leading(num[i][int(length/2):]))
    else:
      res.append(str(int(num[i]) * 2024))
  return res

for i in range(25):
  data = blink(data)

print(len(data))

f.close()
