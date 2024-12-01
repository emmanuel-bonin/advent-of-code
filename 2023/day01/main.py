input_file = open("./input.txt", "r")
lines = input_file.readlines()

result = 0

# Defining written number with their numeric values
NUMBERS = dict({
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
})

def find_number(line, i, find_fn):
    try:
        return int(line[i])
    except:
        for word in NUMBERS:
            if find_fn(word) == i:
                return NUMBERS[word]
    return -1

for line in lines:
    line = line.replace('\n', '')
    a = 0
    b = 0
    for i in range(len(line)):
        n = find_number(line, i, line.find)
        if n != -1:
            a = n
            break
    for i in reversed(range(len(line))):
        n = find_number(line, i, line.rfind)
        if n != -1:
            b = n
            break
    ab = a * 10 + b
    result += ab

print(result)
