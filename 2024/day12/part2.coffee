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
  if lines[i][j] is SEPARATOR
    return currentMap
  if lines[i][j] is c
    currentMap.push([i, j])
    lines[i][j] = SEPARATOR
    if i < lines.length-1 and lines[i+1][j] is c
      createMap(lines[i+1][j], lines, i+1, j, currentMap)
    if i  and lines[i-1][j] is c
      createMap(lines[i-1][j], lines, i-1, j, currentMap)
    if j < lines.length-1 and  lines[i][j+1] is c
      createMap(lines[i][j+1], lines, i, j+1, currentMap)
    if j and lines[i][j-1] is c
      createMap(lines[i][j-1], lines, i, j-1, currentMap)
  return currentMap

inMap = (map, x, y) ->
  return map.find((e) => e[0] is y and e[1] is x)

computeCorners = (map) ->
  corners = []
  for i in [0...map.length]
    corners.push [map[i][0]+.5, map[i][1]+.5] if !corners.find (e) => e[0] is map[i][0]+.5 and e[1] is map[i][1]+.5
    corners.push [map[i][0]-.5, map[i][1]+.5] if !corners.find (e) => e[0] is map[i][0]-.5 and e[1] is map[i][1]+.5
    corners.push [map[i][0]+.5, map[i][1]-.5] if !corners.find (e) => e[0] is map[i][0]+.5 and e[1] is map[i][1]-.5
    corners.push [map[i][0]-.5, map[i][1]-.5] if !corners.find (e) => e[0] is map[i][0]-.5 and e[1] is map[i][1]-.5
  return corners

computeMap = (map) ->
  sides = 0
  corners = computeCorners(map)
  for i in [0...corners.length]
    pos = corners[i]
    [y, x] = pos

    in1 = inMap(map, x-.5, y-.5)
    in2 = inMap(map, x-.5, y+.5)
    in3 = inMap(map, x+.5, y-.5)
    in4 = inMap(map, x+.5, y+.5)

    # is an inside corner
    sides += if (in1 and in2 and in3 and not in4) or
      (in1 and in2 and not in3 and in4) or
      (in1 and not in2 and in3 and in4) or
      (not in1 and in2 and in3 and in4) or
    # is a simple corner
      (in1 and not in2 and not in3 and not in4) or
      (not in1 and in2 and not in3 and not in4) or
      (not in1 and not in2 and in3 and not in4) or
      (not in1 and not in2 and not in3 and in4)
    then 1
    else if (in1 and not in2 and not in3 and in4) or
      (not in1 and in2 and in3 and not in4)
    then 2 else 0

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
