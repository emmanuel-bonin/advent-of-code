input_file = open("./input.txt", "r")
lines = input_file.readlines()

grid = []

for line in lines:
  for i in range(len(line.split())):
    grid.append(line.split()[i])

def count_xmas_at_position(grid, i, j):
  return ((1 if i>2 and j>2 and grid[i-1][j-1] == 'M' and grid[i-2][j-2] == 'A' and grid[i-3][j-3] == 'S' else 0) +
         (1 if i>2 and grid[i-1][j] == 'M' and grid[i-2][j] == 'A' and grid[i-3][j] == 'S' else 0) +
         (1 if i>2 and j<len(grid[i])-3 and grid[i-1][j+1] == 'M' and grid[i-2][j+2] == 'A' and grid[i-3][j+3] == 'S' else 0) +
         (1 if j>2 and grid[i][j-1] == 'M' and grid[i][j-2] == 'A' and grid[i][j-3] == 'S' else 0) +
         (1 if j<len(grid[i])-3 and grid[i][j+1] == 'M' and grid[i][j+2] == 'A' and grid[i][j+3] == 'S' else 0) +
         (1 if i<len(grid)-3 and j>2 and grid[i+1][j-1] == 'M' and grid[i+2][j-2] == 'A' and grid[i+3][j-3] == 'S' else 0) +
         (1 if i<len(grid)-3 and grid[i+1][j] == 'M' and grid[i+2][j] == 'A' and grid[i+3][j] == 'S' else 0) +
         (1 if i<len(grid)-3 and j<len(grid[i])-3 and grid[i+1][j+1] == 'M' and grid[i+2][j+2] == 'A' and grid[i+3][j+3] == 'S' else 0))

result = 0
for i in range(len(grid)):
  for j in range(len(grid[i])):
    if grid[i][j] == 'X':
      result += count_xmas_at_position(grid, i, j)
print(result)
