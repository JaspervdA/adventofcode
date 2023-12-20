from aocd import get_data, submit

year, day = 2023, 11
data = get_data(year=year, day=day).splitlines()
# data = ["...#......",
# ".......#..",
# "#.........",
# "..........",
# "......#...",
# ".#........",
# ".........#",
# "..........",
# ".......#..",
# "#...#....."
# ]

# Find rows with no galaxies
no_galaxy_cols = []
for col in range(len(data[0])):
    no_galaxy = True
    for r in range(len(data)):
        if data[r][col] == "#":
            no_galaxy = False
    if no_galaxy:
        no_galaxy_cols.append(col)

# Find rows with no galaxies and  extract positions of galaxies
no_galaxy_rows = []
galaxy_positions = []
for row_idx, row in enumerate(data):
    no_galaxy = True
    for col_idx, x in enumerate(row):
        if x == "#":
            no_galaxy = False
            galaxy_positions.append([col_idx, row_idx])
    if no_galaxy:
        no_galaxy_rows.append(row_idx)

print("No galaxy rows, cols", no_galaxy_rows, no_galaxy_cols)
print("Galaxy positions", galaxy_positions)

def noGalaxyColsOnRoute(start_galaxy_x, end_galaxy_x):
    lowest_galaxy_x = min(start_galaxy_x, end_galaxy_x)
    highest_galaxy_x = max(start_galaxy_x, end_galaxy_x)

    first_no_galaxy_col = 0
    last_no_galaxy_col = 0
    for col_number, x in enumerate(no_galaxy_cols):
        if lowest_galaxy_x > x:
            first_no_galaxy_col = col_number + 1
            last_no_galaxy_col = first_no_galaxy_col
        elif highest_galaxy_x > x:
            last_no_galaxy_col = col_number +1
    return last_no_galaxy_col - first_no_galaxy_col

def noGalaxyRowsOnRoute(start_galaxy_y, end_galaxy_y):
    lowest_galaxy_y = min(start_galaxy_y, end_galaxy_y)
    highest_galaxy_y = max(start_galaxy_y, end_galaxy_y)
    first_no_galaxy_row = 0
    last_no_galaxy_row = 0
    for row_number, y in enumerate(no_galaxy_rows):
        if lowest_galaxy_y > y:
            first_no_galaxy_row = row_number + 1
            last_no_galaxy_row = first_no_galaxy_row
        elif highest_galaxy_y > y:
            last_no_galaxy_row = row_number + 1
    return last_no_galaxy_row - first_no_galaxy_row

# Calculate shortest route between galaxies
galaxy_age = 1000000
galaxy_age = galaxy_age - 1
def galaxyDistances(galaxy_position):
    galaxy_distance = 0
    for galaxy in galaxy_positions:
        x_dist = abs(galaxy_position[0] - galaxy[0])
        y_dist = abs(galaxy_position[1] - galaxy[1])
        if x_dist == 0 and y_dist == 0:
            galaxy_distance += 0
            # print("same galaxy")
        else:
            galaxy_distance += x_dist + y_dist
            galaxy_distance += galaxy_age * noGalaxyRowsOnRoute(galaxy_position[1], galaxy[1])
            galaxy_distance += galaxy_age * noGalaxyColsOnRoute(galaxy_position[0], galaxy[0])
    return galaxy_distance

total_distance = 0 
count = 0
for galaxy in galaxy_positions:
    total_distance += galaxyDistances(galaxy)
# total_distance += galaxyDistances(galaxy_positions[8])

answerA = int(total_distance / 2)
# print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)


### Part B ###
answerB = int(total_distance / 2)
print("Answer B is", answerB)

submit(answerB, part="b", day=day, year=year)