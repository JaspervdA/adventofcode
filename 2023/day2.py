from aocd import get_data, submit

year = 2023
day = 2

games = get_data(year=year, day=day)
games_per_line = games.splitlines()

count = 0
sum_possible_game_ids = 0
sum_multiples = 0

for game_id, game in enumerate(games_per_line):
    # Count from 0 rather than 10
    game_id += 1
    num_items_to_strip = 6 + len(str(game_id))

    game = game[num_items_to_strip:]
    game = game.replace(" ", "")

    count +=1
    game_items = game.split(';')
    red_min = 0
    green_min = 0
    blue_min = 0
    check = 0
    for game_item in game_items:
        cubes = game_item.split(',')
        for cube in cubes:
            if 'red' in cube:
                red_number = int(cube.replace("red", ""))
                red_min = max(red_min, red_number)
                if red_number > 12:
                    check += 1
            if 'green' in cube:
                green_number = int(cube.replace("green", ""))
                green_min = max(green_min, green_number)
                if green_number > 13:
                    check += 1
            if 'blue' in cube:
                blue_number = int(cube.replace("blue", ""))
                blue_min = max(blue_min, blue_number)
                if blue_number > 14:
                    check += 1
    
    multiple = red_min * blue_min * green_min
    sum_multiples += multiple

    if check > 0:
        print("NOT possible")
    else:
        print('POSSIBLE')
        sum_possible_game_ids += (game_id)


### Part A ###

answerA = sum_possible_game_ids 
# submit(answerA, part="a", day=day, year=year)

### Part B ###

answerB = sum_multiples
# submit(answerB, part="b", day=day, year=year)