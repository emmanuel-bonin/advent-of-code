fs = require 'fs'

parseFile = ->
#  input = fs.readFileSync 'example1.txt', 'utf8'
#  input = fs.readFileSync 'example2.txt', 'utf8'
#  input = fs.readFileSync 'example3.txt', 'utf8'
  input = fs.readFileSync 'input.txt', 'utf8'
  return input.split('\n').filter((l) => l.length).map((l) => l.split(''))

createMap = (c, lines, i, j, currentMap) ->
  if lines[i][j] == '#'
    return currentMap
  if lines[i][j] == c
    currentMap.push([i, j])
    lines[i][j] = '#'
    if i < lines.length - 1 && lines[i+1][j] == c
      createMap(lines[i+1][j], lines, i + 1, j, currentMap)
    if i  && lines[i-1][j] == c
      createMap(lines[i-1][j], lines, i - 1, j, currentMap)
    if j < lines.length - 1 &&  lines[i][j+1] == c
      createMap(lines[i][j+1], lines, i, j + 1, currentMap)
    if j && lines[i][j-1] == c
      createMap(lines[i][j-1], lines, i, j - 1, currentMap)
  return currentMap

computeMap = (map) ->
  total = 0
  for i in [0...map.length]
    total += 4
#    console.log('Getting neighbors for', map[i], 'in', map)
    hn = false
    vn = false
    for j in [0...map.length]
      if i == j
        continue
      hn = false
      vn = false
      if Math.abs(map[i][0] - map[j][0]) == 1 && map[i][1] == map[j][1]
#        console.log('found neighbor for', map[i], 'at', map[j], 'total =>', total, total+2)
        hn = true
        total--
      if Math.abs(map[i][1] - map[j][1]) == 1 && map[i][0] == map[j][0]
#        console.log('found neighbor for', map[i], 'at', map[j], 'total =>', total, total+2)
        vn = true
        total--
#  console.log('borders', total, '*', map.length, '=', total * map.length)
  return total * map.length

main = ->
  lines = parseFile()
  total = 0
  for i in [0...lines.length]
    for j in [0...lines.length]
      if lines[i][j] != '#'
        currentMap = createMap(lines[i][j], lines, i, j, [])
        total += computeMap(currentMap)

  console.log(total)

main()
