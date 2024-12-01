f = open('./input.txt', 'r')
lines = f.readlines()

seed = list()
seed_to_soil = list()
soil_to_fert = list()
fert_to_water = list()
water_to_light = list()
light_to_temp = list()
temp_to_hum = list()
hum_to_loc = list()

for l in lines:
    l = l.replace('\n', '')

SEED_LINE = 0
# SEED_TO_SOIL_LINE = 3
# SOIL_TO_FERT_LINE = 7
# FERT_TO_WATER_LINE = 12
# WATER_TO_LIGHT_LINE = 18
# LIGHT_TO_TEMP_LINE = 22
# TEMP_TO_HUM_LINE = 27
# HUM_TO_LOC_LINE = 31
SEED_TO_SOIL_LINE = 3
SOIL_TO_FERT_LINE = 32
FERT_TO_WATER_LINE = 54
WATER_TO_LIGHT_LINE = 104
LIGHT_TO_TEMP_LINE = 148
TEMP_TO_HUM_LINE = 174
HUM_TO_LOC_LINE = 201


tmp = lines[SEED_LINE].split(' ')
for s in tmp[1:]:
    if len(s):
        seed.append(int(s))

def parse_lines(start, end, list_to_fill):
    i = start
    while i < end:
        tmp = lines[i].split(' ')
        if (len(tmp) > 1):
            list_to_fill.append(dict({ 'dest': int(tmp[0]), 'src': int(tmp[1]), 'len': int(tmp[2]) }))
        i += 1

parse_lines(SEED_TO_SOIL_LINE, SOIL_TO_FERT_LINE - 1, seed_to_soil)
parse_lines(SOIL_TO_FERT_LINE, FERT_TO_WATER_LINE - 1, soil_to_fert)
parse_lines(FERT_TO_WATER_LINE, WATER_TO_LIGHT_LINE - 1, fert_to_water)
parse_lines(WATER_TO_LIGHT_LINE, LIGHT_TO_TEMP_LINE - 1, water_to_light)
parse_lines(LIGHT_TO_TEMP_LINE, TEMP_TO_HUM_LINE - 1, light_to_temp)
parse_lines(TEMP_TO_HUM_LINE, HUM_TO_LOC_LINE - 1, temp_to_hum)
parse_lines(HUM_TO_LOC_LINE, len(lines), hum_to_loc)

def compute(s, m):
    for a in m:
        if s >= a['src'] and s < a['src'] + a['len']:
            diff = s - a['src']
            return a['dest'] + diff
    return s

low = 0
for s in seed:
    soil = compute(s, seed_to_soil)
    fert = compute(soil, soil_to_fert)
    water = compute(fert, fert_to_water)
    light = compute(water, water_to_light)
    temp = compute(light, light_to_temp)
    hum = compute(temp, temp_to_hum)
    loc = compute(hum ,hum_to_loc)
    if low == 0:
        low = loc
    else:
        low = min(low, loc)
print('lowest loc', low)
