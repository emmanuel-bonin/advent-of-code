from sympy import symbols, Eq, solve, core

f = open('./input.txt', 'r')

lines = f.readlines()


def compute(button_a, button_b, prize):
    x, y = symbols('x y')
    eq1 = Eq(button_a[0] * x + button_b[0] * y, prize[0])
    eq2 = Eq(button_a[1] * x + button_b[1] * y, prize[1])
    solution = solve((eq1, eq2), (x, y))
    [a, b] = list(solution.values())
    if type(a) is core.numbers.Integer and type(b) is core.numbers.Integer:
        return a * 3 + b
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
            prize = (10000000000000 + int(raw_prize[0].split('=')[1]), 10000000000000 + int(raw_prize[1].split('=')[1]))
            t = compute(button_a, button_b, prize)
            total += t
    print(total)


main()
