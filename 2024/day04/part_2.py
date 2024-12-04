input_file = open("./input.txt", "r")
lines = input_file.readlines()

grid = []
words = []

for line in lines:
  for i in range(len(line.split())):
    grid.append(line.split()[i])

def find_x_mas(grid, i, j):
  found_tl = False
  found_tr = False
  found_bl = False
  found_br = False

  if i > 0 and j > 0 and (grid[i-1][j-1] == 'M' or grid[i-1][j-1] == 'S'):
    found_tl = grid[i-1][j-1]
  if i > 0 and j < len(grid[i]) - 1 and (grid[i-1][j+1] == 'M' or grid[i-1][j+1] == 'S'):
    found_tr = grid[i-1][j+1]
  if i < len(grid) - 1 and j > 0 and (grid[i+1][j-1] == 'M' or grid[i+1][j-1] == 'S'):
    found_bl = grid[i+1][j-1]
  if i < len(grid) - 1 and j < len(grid[i]) - 1 and (grid[i+1][j+1] == 'M' or grid[i+1][j+1] == 'S'):
    found_br = grid[i+1][j+1]
  possible_solutions = [
    ['M', 'S', 'M', 'S'],
    ['S', 'M', 'S', 'M'],
    ['M', 'S', 'S', 'M'],
    ['S', 'M', 'M', 'S']
  ]
  for solution in possible_solutions:
    if solution[0] == found_tl and solution[1] == found_br and solution[2] == found_bl and solution[3] == found_tr:
      return True
  return False

result = 0
for i in range(len(grid)):
  for j in range(len(grid[i])):
    if grid[i][j] == 'A':
      if find_x_mas(grid, i, j):
        result += 1
print(result)
