input_file = open("./input.txt", "r")

games = input_file.readlines()

result = 0

MAX_CUBES = dict({
    'red': 12,
    'green': 13,
    'blue': 14
})

for game in games:
    game = game.replace('\n', '')
    game_name = game.split(":")[0]
    game_id = int(game_name.split(" ")[1])
    game_iterations = game.strip().split(":")[1].strip().split(";")
    is_valid = True
    for iteration in game_iterations:
        cubes = iteration.strip().split(", ")
        for cube in cubes:
            n = int(cube.split(' ')[0])
            color = cube.split(' ')[1]
            if n > MAX_CUBES[color]:
                is_valid = False
                break
        if is_valid == False:
            break
    if is_valid == True:
        result += game_id
print(f'result = {result}')
