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
    if i < lines.length - 1 && lines[i+1][j] == c
      createMap(lines[i+1][j], lines, i + 1, j, currentMap)
    if i  && lines[i-1][j] == c
      createMap(lines[i-1][j], lines, i - 1, j, currentMap)
    if j < lines.length - 1 &&  lines[i][j+1] == c
      createMap(lines[i][j+1], lines, i, j + 1, currentMap)
    if j && lines[i][j-1] == c
      createMap(lines[i][j-1], lines, i, j - 1, currentMap)
  return currentMap

genKey = (i, j) ->
  return i + ',' + j

inMap = (map, x, y) ->
  return map.find((e) => e[0] == y && e[1] == x)

computeCorner = (corners, map, i) ->
  y = map[i][0]
  x = map[i][1]
  key1 = genKey(y+.5, x+.5)
  key2 = genKey(y-.5, x+.5)
  key3 = genKey(y+.5, x-.5)
  key4 = genKey(y-.5, x-.5)
  if !corners.includes(key1)
    corners.push key1
  if !corners.includes(key2)
    corners.push key2
  if !corners.includes(key3)
    corners.push key3
  if !corners.includes(key4)
    corners.push key4

computeMap = (map) ->
  sides = 0
  corners = []
  for i in [0...map.length]
    computeCorner(corners, map, i)
  cornerPos = Object.values(corners)
  for i in [0...cornerPos.length]
    pos = cornerPos[i].split(',').map parseFloat

    # x1y1 | x3y3
    # -----o-----
    # x2y2 | x4y4
    [y1, x1] = [Number(pos[0]-.5), Number(pos[1]-.5)]
    [y2, x2] = [Number(pos[0]+.5), Number(pos[1]-.5)]
    [y3, x3] = [Number(pos[0]-.5), Number(pos[1]+.5)]
    [y4, x4] = [Number(pos[0]+.5), Number(pos[1]+.5)]
    in1 = inMap(map, x1, y1)
    in2 = inMap(map, x2, y2)
    in3 = inMap(map, x3, y3)
    in4 = inMap(map, x4, y4)
    # corner is in middle of 3 cases
    if (in1 && in2 && in3 && !in4) || (in1 && in2 && !in3 && in4) || (in1 && !in2 && in3 && in4) || (!in1 && in2 && in3 && in4)
      sides += 1
    # corner is in middle of 2 diagonally aligned cases
    else if (in1 && !in2 && !in3 && in4) || (!in1 && in2 && in3 && !in4)
      sides += 2
    # corner is just a corner
    else if (in1 && !in2 && !in3 && !in4) || (!in1 && in2 && !in3 && !in4) || (!in1 && !in2 && in3 && !in4) || (!in1 && !in2 && !in3 && in4)
      sides += 1
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
