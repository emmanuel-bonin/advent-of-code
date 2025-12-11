def compute_sequence(machine):
    print(machine)
    return 0

def main():
    f = open('example.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    f.close()

    machines = []
    for line in lines:
        group_str = line.split(' ')
        lights_schema = group_str.pop(0).replace('[', '').replace(']', '')
        button_groups = []
        for s in group_str:
            if s[0] == '(':
                button_groups.append([int(x) for x in s.replace('(', '').replace(')', '').split(',')])
        machines.append({ 'lights_schema': lights_schema, 'button_groups': button_groups })
    res = 0
    for machine in machines:
        res += compute_sequence(machine)
    print(res)

main()
