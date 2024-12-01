SEED_LINE = 0

# f = open('./example.txt', 'r')
# SEED_TO_SOIL_LINE = 3
# SOIL_TO_FERT_LINE = 7
# FERT_TO_WATER_LINE = 12
# WATER_TO_LIGHT_LINE = 18
# LIGHT_TO_TEMP_LINE = 22
# TEMP_TO_HUM_LINE = 27
# HUM_TO_LOC_LINE = 31

f = open('./input.txt', 'r')
SEED_TO_SOIL_LINE = 3
SOIL_TO_FERT_LINE = 32
FERT_TO_WATER_LINE = 54
WATER_TO_LIGHT_LINE = 104
LIGHT_TO_TEMP_LINE = 148
TEMP_TO_HUM_LINE = 174
HUM_TO_LOC_LINE = 201

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

tmp_seed = list()
tmp = lines[SEED_LINE].split(' ')
for s in tmp[1:]:
    if len(s):
        tmp_seed.append(int(s))

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

i = 0
seed_ranges = list()
while i < len(tmp_seed):
    start_seed = tmp_seed[i]
    len_seed = tmp_seed[i+1]
    seed_ranges.append(dict({ 'src': start_seed, 'len': len_seed }))
    i += 2

def compute_new_seeds(seeds_ranges_raw, compute_map):
    seeds_ranges = seeds_ranges_raw.copy()
    new_ranges = list()
    for s in seeds_ranges:
        matched = False
        for m in compute_map:
            start_seed = s['src']
            end_seed = s['src'] + s['len']
            start_map = m['src']
            end_map = m['src'] + m['len']

            # seed:      |------|
            # map:   |--------------|
            # take:      |------|
            # diff:  |...|
            # si depart seed entre source et source+len de map
            # et fin seed entre source et source+len de map
            # on compute et ajoute le nouveau point de depart dans les nouvelles seed
            if start_seed >= start_map and start_seed < end_map and end_seed <= end_map:
                matched = True
                diff = start_seed - start_map
                new_ranges.append(dict({ 'src': m['dest'] + diff, 'len': s['len'] }))
                break

            # seed: |------------------|
            # map:      |--------|
            # take: |...|--------|.....|
            # si seed commence avant map et fini apres map
            # on ajoute ce qui est avant map
            # on compute et ajoute de qui est dans map
            # on ajoute ce qui est apres map
            elif start_seed < start_map and end_seed > end_map:
                matched = True
                seeds_ranges.append(dict({ 'src': start_seed, 'len': start_map - start_seed }))
                new_ranges.append(dict({ 'src': m['dest'], 'len': m['len'] }))
                seeds_ranges.append(dict({ 'src': end_map, 'len': end_seed - end_map }))
                break

            # seed: |--------------|
            # map:      |-------------|
            # take: |...|----------|
            # si depart seed avant source de map
            # et fin seed entre source et source+len de map
            # on ajoute ce qui est avant map dans les nouvelles seed
            # et on compute et ajoute ce qui est entre source et source+len
            elif start_seed <= start_map and end_seed >= start_map and end_seed <= end_map:
                matched = True
                seeds_ranges.append(dict({ 'src': start_seed, 'len': start_map - start_seed }))
                new_ranges.append(dict({ 'src': m['dest'], 'len': end_seed - start_map }))
                break

            # seed:     |--------------|
            # map:   |-----------|
            # take:     |--------|.....|
            # diff:  |..|
            # si depart seed entre source et source+len de map
            # et fin seed apres source et source+len de map
            # on compute et ajoute ce qui est entre source et source+len
            # et on ajoute ce qui est apres fin de map
            elif start_seed >= start_map and start_seed <= end_map and end_seed >= end_map:
                matched = True
                diff = start_seed - start_map
                new_ranges.append(dict({ 'src': m['dest'] + diff, 'len': end_map - start_seed }))
                seeds_ranges.append(dict({ 'src': end_map, 'len': end_seed - end_map }))
                break

        if matched == False:
            new_ranges.append(s)
    return new_ranges

import json

# print('seed to soil with', json.dumps(seed_ranges, indent=2))
new_seeds = compute_new_seeds(seed_ranges, seed_to_soil)
# print('soil to fert', json.dumps(new_seeds, indent=2))
new_seeds = compute_new_seeds(new_seeds, soil_to_fert)
# print('fert to water', json.dumps(new_seeds, indent=2))
new_seeds = compute_new_seeds(new_seeds, fert_to_water)
# print('water to light', json.dumps(new_seeds, indent=2))
new_seeds = compute_new_seeds(new_seeds, water_to_light)
# print('light to temp', json.dumps(new_seeds, indent=2))
new_seeds = compute_new_seeds(new_seeds, light_to_temp)
# print('temp to hum', json.dumps(new_seeds, indent=2))
new_seeds = compute_new_seeds(new_seeds, temp_to_hum)
# print('hum to loc', json.dumps(new_seeds,indent=2))
new_seeds = compute_new_seeds(new_seeds, hum_to_loc)
# print('new', json.dumps(new_seeds, indent=2))

low = None
for s in new_seeds:
    if low == None:
        low = s['src']
    else:
    # elif s['src'] != 0:
        low=min(low, s['src'])
print('low =', low)
