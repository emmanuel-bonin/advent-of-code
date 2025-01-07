f = open('./input.txt', 'r')

lines = f.readlines()


def compute(button_a, button_b, prize):
    finished = False
    nb_a = prize[0] // button_a[0]
    nb_b = 1
    while not finished:
        while nb_a * button_a[0] + nb_b * button_b[0] < prize[0]:
            nb_b += 1
        if nb_a * button_a[0] + nb_b * button_b[0] == prize[0]:
            if nb_a * button_a[1] + nb_b * button_b[1] == prize[1]:
                return nb_a * 3 + nb_b
            else:
                nb_a -= 1
                if nb_a < 0:
                    finished = True
                    break
        else:
            nb_a -= 1
            if nb_a < 0:
                finished = True
                break
    if nb_a * button_a[0] + nb_b * button_b[0] == prize[0]:
        if nb_a * button_a[1] + nb_b * button_b[1] == prize[1]:
            return nb_a * 3 + nb_b
    return 0


def main():
    button_a = (0, 0)
    button_b = (0, 0)
    prize = (0, 0)
    total = 0
    for line in lines:
        if "Button" in line:
            raw_xy = [s.strip() for s in line.split(':')[1].split(',')]
            if "A" in line:
                button_a = (int(raw_xy[0].split('+')[1]), int(raw_xy[1].split('+')[1]))
            elif "B" in line:
                button_b = (int(raw_xy[0].split('+')[1]), int(raw_xy[1].split('+')[1]))
        elif "Prize" in line:
            raw_prize = [s.strip() for s in line.split(':')[1].split(',')]
            prize = (int(raw_prize[0].split('=')[1]), int(raw_prize[1].split('=')[1]))
            t = compute(button_a, button_b, prize)
            total += t
    print(total)


main()
