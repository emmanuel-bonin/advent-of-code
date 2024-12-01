# Time:        63789468
# Distance:   411127420471035

# Time:      71530
# Distance:  940200

# races = [
#   dict({
#     'time': 71530,
#     'distance': 940200
#   }),
# ]

races = [
  dict({
    'time': 63789468,
    'distance': 411127420471035
  })
]

result = 0
for race in races:
  ways_to_win = 0
  for i in range(race['time']):
    speed = i
    time_to_move = race['time'] - i
    distance = time_to_move * speed
    if distance > race['distance']:
      ways_to_win += 1
  if result == 0:
    result = ways_to_win
  else:
    result *= ways_to_win
  print('temporary result', result)
print(result)
