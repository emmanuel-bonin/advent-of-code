input_file = open("./input.txt", "r")
lines = input_file.readlines()

grid = []
words = []

for line in lines:
  for i in range(len(line.split())):
    grid.append(line.split()[i])

Direction = dict({
  0: 'TL',
  1: 'T',
  2: 'TR',
  3: 'L',
  4: 'R',
  5: 'BL',
  6: 'B',
  7: 'BR'
})

def find_vectors(grid, i, j, letter, direction):
  next_letter = 'M' if letter == 'X' else 'A' if letter == 'M' else 'S' if letter == 'A' else ''

  # we found the last letter
  if next_letter == '':
    return (i, j, direction)

  if direction == Direction[0] and i > 0 and j > 0 and grid[i-1][j-1] == next_letter:
    return find_vectors(grid, i-1, j-1, next_letter, direction)
  elif direction == Direction[1] and i > 0 and grid[i-1][j] == next_letter:
    return find_vectors(grid, i-1, j, next_letter, direction)
  elif direction == Direction[2] and i > 0 and j < len(grid[i]) - 1 and grid[i-1][j+1] == next_letter:
    return find_vectors(grid, i-1, j+1, next_letter, direction)
  elif direction == Direction[3] and j > 0 and grid[i][j-1] == next_letter:
    return find_vectors(grid, i, j-1, next_letter, direction)
  elif direction == Direction[4] and j < len(grid[i]) - 1 and grid[i][j+1] == next_letter:
    return find_vectors(grid, i, j+1, next_letter, direction)
  elif direction == Direction[5] and i < len(grid) - 1 and j > 0 and grid[i+1][j-1] == next_letter:
    return find_vectors(grid, i+1, j-1, next_letter, direction)
  elif direction == Direction[6] and i < len(grid) - 1 and grid[i+1][j] == next_letter:
    return find_vectors(grid, i+1, j, next_letter, direction)
  elif direction == Direction[7] and i < len(grid) - 1 and j < len(grid[i]) - 1 and grid[i+1][j+1] == next_letter:
    return find_vectors(grid, i+1, j+1, next_letter, direction)
  return (-1, -1, -1)

result = 0
for i in range(len(grid)):
  for j in range(len(grid[i])):
    if grid[i][j] == 'X':
      if (find_vectors(grid, i, j, 'X', Direction[0]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[1]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[2]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[3]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[4]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[5]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[6]) != (-1, -1, -1)):
        result += 1
      if (find_vectors(grid, i, j, 'X', Direction[7]) != (-1, -1, -1)):
        result += 1
print(result)
