import re

# f = open('input.txt', 'r')
f = open('example.txt', 'r')

lines = f.readlines()
f.close()

numeric_keys = {
    '7': {'x': 0, 'y': 0}, '8': {'x': 1, 'y': 0}, '9': {'x': 2, 'y': 0},
    '4': {'x': 0, 'y': 1}, '5': {'x': 1, 'y': 1}, '6': {'x': 2, 'y': 1},
    '1': {'x': 0, 'y': 2}, '2': {'x': 1, 'y': 2}, '3': {'x': 2, 'y': 2},
    'X': {'x': 0, 'y': 3}, '0': {'x': 1, 'y': 3}, 'A': {'x': 2, 'y': 3},
}

directional_keys = {
    'X': {'x': 0, 'y': 0}, '^': {'x': 1, 'y': 0}, 'A': {'x': 2, 'y': 0},
    '<': {'x': 0, 'y': 1}, 'v': {'x': 1, 'y': 1}, '>': {'x': 2, 'y': 1},
}


def get_directional_sequence(start, end):
    start_key = directional_keys[start]
    end_key = directional_keys[end]
    diffx = end_key['x'] - start_key['x']
    diffy = end_key['y'] - start_key['y']
    seq = ''
    if start_key['x'] + diffx == 0 and start_key['y'] == 0:
        seq += 'v' * abs(diffy)
        diffy = 0
    if start_key['y'] + diffy == 0 and start_key['x'] == 0:
        seq += '>' * abs(diffx)
        diffx = 0

    seq1 = seq + ('>' if diffx > 0 else '<') * abs(diffx) + ('v' if diffy > 0 else '^') * abs(diffy)
    seq2 = seq + ('v' if diffy > 0 else '^') * abs(diffy) + ('>' if diffx > 0 else '<') * abs(diffx)
    print('[dir]:', len(seq1), len(seq2))
    return (seq1 if len(seq1) < len(seq2) else seq2) + 'A'


def get_numeric_sequence(start, end):
    start_key = numeric_keys[start]
    end_key = numeric_keys[end]
    diffx = end_key['x'] - start_key['x']
    diffy = end_key['y'] - start_key['y']
    seq = ''
    if start_key['x'] + diffx == 0 and start_key['y'] == 3:
        seq += '^' * abs(diffy)
        diffy = 0
    if start_key['y'] + diffy == 3 and start_key['x'] == 0:
        seq += '>' * abs(diffx)
        diffx = 0

    # Bug comes from here: IDK why when switching the order of x and y being generated it works or not
    seq1 = seq + ('>' if diffx > 0 else '<') * abs(diffx) + ('v' if diffy > 0 else '^') * abs(diffy)
    seq2 = seq + ('v' if diffy > 0 else '^') * abs(diffy) + ('>' if diffx > 0 else '<') * abs(diffx)
    print('[num]:', len(seq1), len(seq2))
    return (seq1 if len(seq1) < len(seq2) else seq2) + 'A'


total = 0
for line in lines:
    dir_seq = ''
    _seq_1 = ''
    _seq_2 = ''
    _seq_3 = ''
    line = 'A' + line.strip('\n')
    for i in range(len(line) - 1):
        #     print('Getting numeric sequence of', line[i], '->', line[i + 1], end='')
        num_seq = get_numeric_sequence(line[i], line[i + 1])
        #     print('\t=>', num_seq)
        num_seq = 'A' + num_seq
        _seq_1 += num_seq
        for j in range(len(num_seq) - 1):
            #       print('\t[1] Getting directional sequence of', num_seq[j], '->', num_seq[j + 1], end='')
            dir_seq_1 = get_directional_sequence(num_seq[j], num_seq[j + 1])
            #       print('\t=>', dir_seq_1)
            dir_seq_1 = 'A' + dir_seq_1
            _seq_2 += dir_seq_1
            for k in range(len(dir_seq_1) - 1):
                #         print('\t\t[2] Getting directional sequence of', dir_seq_1[k], '->', dir_seq_1[k + 1], end='')
                dir_seq_2 = get_directional_sequence(dir_seq_1[k], dir_seq_1[k + 1])
                #         print('\t=>', dir_seq_2)
                dir_seq += dir_seq_2
                _seq_3 += dir_seq_2
    if line.startswith('A'):
        line = line[1:]
    m = re.match(r'\d+', line)
    total += int(m.group()) * len(dir_seq)
    print(int(m.group()), '*', len(dir_seq), '=', int(m.group()) * len(dir_seq))
    print(_seq_3)
    print(_seq_2)
    print(_seq_1)
    print(line)

print(total)

# [OK] 379A: v<<A>>^AvA^Av<A<AA>>^AAvA^<A>AAvA^Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A
# [KO] 379A: v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A
