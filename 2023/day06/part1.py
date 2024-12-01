# Time:        63     78     94     68
# Distance:   411   1274   2047   1035

# Time:      7  15   30
# Distance:  9  40  200

# races = [
#   dict({
#     'time': 7,
#     'distance': 9
#   }),
#   dict({
#     'time': 15,
#     'distance':40
#   }),
#     dict({
#     'time': 30,
#     'distance': 200
#   }),
# ]

races = [
  dict({
    'time': 63,
    'distance': 411
  }),
  dict({
    'time': 78,
    'distance':1274
  }),
  dict({
    'time': 94,
    'distance': 2047
  }),
  dict({
    'time': 68,
    'distance': 1035
  })
]

result = 0
for race in races:
  ways_to_win = 0
  for i in range(race['time']):
    speed = i
    time_to_move = race['time'] - i
    distance = time_to_move * speed
    print('pressing', i, 'ms gives speed', speed, 'and', time_to_move, 'ms to move on', distance)
    if distance > race['distance']:
      ways_to_win += 1
      print(ways_to_win)
  if result == 0:
    result = ways_to_win
  else:
    result *= ways_to_win
  print('temporary result', result)
print(result)
