input_file = open("./input.txt", "r")
#input_file = open("./example.txt", "r")

games = input_file.readlines()

result = 0

for game in games:
    game = game.replace('\n', '')
    game_name = game.split(":")[0]
    game_id = int(game_name.split(" ")[1])
    game_iterations = game.strip().split(":")[1].strip().split(";")

    mini = dict({
        'red': -1,
        'green': -1,
        'blue': -1
    })
    for iteration in game_iterations:
        cubes = iteration.strip().split(", ")
        for cube in cubes:
            n = int(cube.split(' ')[0])
            color = cube.split(' ')[1]
            if mini[color] == -1 or n > mini[color]:
                mini[color] = n
#    print('mini cubes for game ' + str(game_id) + ' => red: ' + str(mini['red']) + ' green: ' + str(mini['green']) + ' blue: ' + str(mini['blue']))
    power = mini['red'] * mini['green'] * mini['blue']
    result += power
print(f'result = {result}')
