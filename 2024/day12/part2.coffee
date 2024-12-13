fs = require 'fs'

parseFile = ->
#  input = fs.readFileSync 'example1.txt', 'utf8'
#  input = fs.readFileSync 'example2.txt', 'utf8'
#  input = fs.readFileSync 'example3.txt', 'utf8'
#  input = fs.readFileSync 'example4.txt', 'utf8'
#  input = fs.readFileSync 'example5.txt', 'utf8'
#  input = fs.readFileSync 'example6.txt', 'utf8'
  input = fs.readFileSync 'input.txt', 'utf8'
  return input.split('\n').filter((l) => l.length).map((l) => l.split(''))

SEPARATOR = '.'

createMap = (c, lines, i, j, currentMap) ->
  if lines[i][j] == SEPARATOR
    return currentMap
  if lines[i][j] == c
    currentMap.push([i, j])
    lines[i][j] = SEPARATOR
    if i < lines.length - 1 and lines[i+1][j] == c
      createMap(lines[i+1][j], lines, i + 1, j, currentMap)
    if i  and lines[i-1][j] == c
      createMap(lines[i-1][j], lines, i - 1, j, currentMap)
    if j < lines.length - 1 and  lines[i][j+1] == c
      createMap(lines[i][j+1], lines, i, j + 1, currentMap)
    if j and lines[i][j-1] == c
      createMap(lines[i][j-1], lines, i, j - 1, currentMap)
  return currentMap

genKey = (i, j) ->
  return i + ',' + j

inMap = (map, x, y) ->
  return map.find((e) => e[0] == y and e[1] == x)

computeCorner = (corners, map, i) ->
  y = map[i][0]
  x = map[i][1]
  [y1, x1] = [y+.5, x+.5]
  [y2, x2] = [y-.5, x+.5]
  [y3, x3] = [y+.5, x-.5]
  [y4, x4] = [y-.5, x-.5]
  corners.push [y1, x1] if !corners.find (e) => e[0] == y1 and e[1] == x1
  corners.push [y2, x2] if !corners.find (e) => e[0] == y2 and e[1] == x2
  corners.push [y3, x3] if !corners.find (e) => e[0] == y3 and e[1] == x3
  corners.push [y4, x4] if !corners.find (e) => e[0] == y4 and e[1] == x4

computeMap = (map) ->
  sides = 0
  corners = []
  for i in [0...map.length]
    computeCorner(corners, map, i)
  cornerPos = Object.values(corners)
  for i in [0...corners.length]
    pos = corners[i]
    [y, x] = pos

    # x1y1 | x3y3
    # -----o-----
    # x2y2 | x4y4
    [y1, x1] = [y-.5, x-.5]
    [y2, x2] = [y+.5, x-.5]
    [y3, x3] = [y-.5, x+.5]
    [y4, x4] = [y+.5, x+.5]
    in1 = inMap(map, x1, y1)
    in2 = inMap(map, x2, y2)
    in3 = inMap(map, x3, y3)
    in4 = inMap(map, x4, y4)
    sides += if (in1 and in2 and in3 and not in4) or
      # os an inside corner
      (in1 and in2 and not in3 and in4) or
      (in1 and not in2 and in3 and in4) or
      (not in1 and in2 and in3 and in4) or
      # os a simple corner
      (in1 and not in2 and not in3 and not in4) or
      (not in1 and in2 and not in3 and not in4) or
      (not in1 and not in2 and in3 and not in4) or
      (not in1 and not in2 and not in3 and in4)
    then 1 else 0
    sides += if (in1 and not in2 and not in3 and in4) or (not in1 and in2 and in3 and not in4) then 2 else 0

  return sides * map.length

debugMap = (map) ->
  for i in [0...map.length]
    console.log(map[i].join(''))

main = ->
  lines = parseFile()
  total = 0
  finished = false
  while !finished
    finished = true
    for i in [0...lines.length]
      for j in [0...lines[i].length]
        if lines[i][j] != SEPARATOR
          c = lines[i][j]
          currentMap = createMap(c, lines, i, j, [])
          mapRes = computeMap(currentMap)
          total += mapRes
          finished = false
          break
      if !finished
        break
  console.log(total)

main()
