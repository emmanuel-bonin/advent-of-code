input_file = open("./input.txt", "r")
lines = input_file.readlines()
input_file.close()

dial_pos = 50
res = 0

for line in lines:
    n = int(line[1:])
    if n >= 100:
        # Computing when turning the dial for more than 100
        # we simply increase the number of times passing by 0
        # and subtract hundreds to the base number
        # to keep only the amount of times we should really turn
        res += int(abs(n) / 100)
        n %= 100
    if line[0] == "L":
        # This condition handles a passing by zero
        if dial_pos - n < 0:
            # if we were not on 0 and go below 0, we increase the "passing by 0" counter
            # this condition is there to prevent counter increase again in case we stopped on 0 at previous loop
            if dial_pos > 0:
                res += 1
            # set new dial position
            dial_pos = dial_pos - n + 100
        else:
            # no specific case, simply compute new position
            dial_pos -= n
    elif line[0] == "R":
        # This condition handles a passing by 0
        if dial_pos + n > 99:
            # if we were not on 99, we increase the "passing by 0" counter
            # this condition is there to prevent counter increase again in case we stopped on 0 at previous loop
            if dial_pos + n > 100:
                res += 1
            # computing new dial position
            dial_pos = dial_pos + n - 100
        else:
            # no specific case, simply compute new position
            dial_pos += n
    # if dial stops by 0, increase counter
    if dial_pos == 0:
        res += 1

print(res)
