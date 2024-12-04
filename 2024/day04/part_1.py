input_file = open("./input.txt", "r")
lines = input_file.readlines()

grid = []
words = []

for line in lines:
  for i in range(len(line.split())):
    grid.append(line.split()[i])

def find_vectors(grid, i, j, letter, direction):
  next_letter = 'M' if letter == 'X' else 'A' if letter == 'M' else 'S' if letter == 'A' else ''

  # we found the last letter
  if next_letter == '':
    return 1

  if direction == 0 and i > 0 and j > 0 and grid[i-1][j-1] == next_letter:
    return find_vectors(grid, i-1, j-1, next_letter, direction)
  elif direction == 1 and i > 0 and grid[i-1][j] == next_letter:
    return find_vectors(grid, i-1, j, next_letter, direction)
  elif direction == 2 and i > 0 and j < len(grid[i]) - 1 and grid[i-1][j+1] == next_letter:
    return find_vectors(grid, i-1, j+1, next_letter, direction)
  elif direction == 3 and j > 0 and grid[i][j-1] == next_letter:
    return find_vectors(grid, i, j-1, next_letter, direction)
  elif direction == 4 and j < len(grid[i]) - 1 and grid[i][j+1] == next_letter:
    return find_vectors(grid, i, j+1, next_letter, direction)
  elif direction == 5 and i < len(grid) - 1 and j > 0 and grid[i+1][j-1] == next_letter:
    return find_vectors(grid, i+1, j-1, next_letter, direction)
  elif direction == 6 and i < len(grid) - 1 and grid[i+1][j] == next_letter:
    return find_vectors(grid, i+1, j, next_letter, direction)
  elif direction == 7 and i < len(grid) - 1 and j < len(grid[i]) - 1 and grid[i+1][j+1] == next_letter:
    return find_vectors(grid, i+1, j+1, next_letter, direction)
  return 0

result = 0
for i in range(len(grid)):
  for j in range(len(grid[i])):
    if grid[i][j] == 'X':
      result += find_vectors(grid, i, j, 'X', 0)
      result += find_vectors(grid, i, j, 'X', 1)
      result += find_vectors(grid, i, j, 'X', 2)
      result += find_vectors(grid, i, j, 'X', 3)
      result += find_vectors(grid, i, j, 'X', 4)
      result += find_vectors(grid, i, j, 'X', 5)
      result += find_vectors(grid, i, j, 'X', 6)
      result += find_vectors(grid, i, j, 'X', 7)
print(result)
