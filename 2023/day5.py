from aocd import get_data, submit

year, day = 2023, 5

data = get_data(year=year, day=day).splitlines()

### Part A ###

# data = ["seeds: 79 14 55 13",
# "",
# "seed-to-soil map:",
# "50 98 2",
# "52 50 48",
# "",
# "soil-to-fertilizer map:",
# "0 15 37",
# "37 52 2",
# "39 0 15",
# "",
# "fertilizer-to-water map:",
# "49 53 8",
# "0 11 42",
# "42 0 7",
# "57 7 4",
# "",
# "water-to-light map:",
# "88 18 7",
# "18 25 70",
# "",
# "light-to-temperature map:",
# "45 77 23",
# "81 45 19",
# "68 64 13",
# "",
# "temperature-to-humidity map:",
# "0 69 1",
# "1 0 69",
# "",
# "humidity-to-location map:",
# "60 56 37",
# "56 93 4"
# ]

mappings = []
mapping = []
line_count = len(data)
for line_idx, line in enumerate(data):
    seeds_list = []
    if line_idx == 0:
        seeds = line.split(":")[1]
        seeds = seeds[1:].split(" ")

        seed_mapping = []
        seed_map = ""
        for idx, seed in enumerate(seeds):
            if idx%2 == 0:
                seed_map += seed + " " + seed
            else:
                seed_map += " " + seed
                seed_mapping.append(seed_map)
                seed_map = ""
        mappings.append(seed_mapping)
        continue
    
    if line == "":
        if len(mapping) > 0:
            mappings.append(mapping)
            mapping = []
    elif line[-1] != ":":
        mapping.append(line)
    if line_idx == (line_count - 1):
        mappings.append(mapping)


def mapNewNumber(old_number, mapping):
    new_number = old_number
    for map in mapping:
        map_split = map.split(" ")
        range_start = int(map_split[1])
        range_length  = int(map_split[2])
        destination_start = int(map_split[0])
        if (old_number - range_start) > -1 and old_number < (range_start + range_length):
            new_number = destination_start + (old_number - range_start)
    
    return new_number


locations = []
for seed_number in seeds:
    # For part A
    new_number = int(seed_number)
    for x in range(len(mappings)):
        new_number = mapNewNumber(new_number, mappings[x])
    locations.append(new_number)

answerA = min(locations)
print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def seedNumberInStartRange(seed_number):
    seed_mapping = mappings[0]
    check = False
    for map in seed_mapping:
        map_split = map.split(" ")
        range_start = int(map_split[1])
        range_length  = int(map_split[2])
        if (seed_number - range_start) > -1 and seed_number < (range_start + range_length):
            check = True
    return check

def findMinLocation(seed_numbers):
    min_seed_number = 0
    locations = []
    min_location = 10987654321

    for seed_number in seed_numbers:
        new_number = seed_number
        for x in range(len(mappings)):
            new_number = mapNewNumber(new_number, mappings[x])
        if seedNumberInStartRange(seed_number):
            # print('seed number in starting range', seed_number)
            if new_number < min_location:
                min_location = new_number
                min_seed_number = seed_number
            locations.append(new_number)

    return min_seed_number, min_location


loop_power = [9,8,7,6,5,4]
min_seed_number = 0
min_locations = []
for seed in seeds:
    min_seed_number = int(seed)
    for i in loop_power:
        loop_start = int(max(0, min_seed_number - pow(10,i) ))
        seed_numbers_search = [x for x in range(loop_start, loop_start + pow(10,i), pow(10,i-4))]
        min_seed_number, min_location = findMinLocation(seed_numbers_search)
        print(min_seed_number, min_location)
    min_locations.append(min_location)

answerB = min(min_locations)
print("Answer B is", answerB)

submit(answerB, part="b", day=day, year=year)