from aocd import get_data, submit
import math

year, day = 2023, 21
data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".split("\n")
data = get_data(year=year, day=day).splitlines()
grid_size = len(data)

parsed_data = [[None for x in range(grid_size)] for y in range(grid_size)]
# Parse the data 
for y, row in enumerate(data):
    for x, col in enumerate(row):
        parsed_data[x][y] = col
        if col == "S":
            start_position = [x,y]
            parsed_data[x][y] = "."

def getDifferences(list_of_values):
    differences = []
    for index, current_value in enumerate(list_of_values):
        if index == 0:
            last_value = current_value
        else:
            differences.append(current_value - last_value)
            last_value = current_value
    return differences

def checkAllZeroes(sequence):
    return all(v == 0 for v in sequence)

def expandStartGrid(start_grid, start_position, expansion_factor):
    expanded_start_position = [start_position[0] + grid_size * expansion_factor, start_position[1] + grid_size * expansion_factor]
    expanded_grid = []
    for i in range(1 + expansion_factor * 2):
        for row in start_grid:
            expanded_grid.append(row * (1 + expansion_factor * 2))
    return expanded_grid, expanded_start_position

# Get next positions. Store 
def getNextPositions(current_position, expansion_factor):
    odd_even, x, y = current_position[0], current_position[1], current_position[2]
    next_positions = []
    next_odd_even = "odd" if odd_even == "even" else "even"
    # Try moving left if we are not at the edge
    if x > 0:
        # Only move left if it is not a rock and we have not seen this position before
        if parsed_data[x-1][y] != "#" and not seen_positions[x-1][y][odd_even]:
            # Also set if we are at an odd or even move
            seen_positions[x-1][y][odd_even] = True
            next_positions.append([next_odd_even, x-1, y])
        
    # Try moving right
    if x < (grid_size -1 + grid_size * 2 * expansion_factor):
        # Only move left if it is not a rock and we have not seen this position before
        if parsed_data[x+1][y] != "#" and not seen_positions[x+1][y][odd_even]:
            # Also set if we are at an odd or even move
            seen_positions[x+1][y][odd_even] = True
            next_positions.append([next_odd_even, x+1, y])

    # Try moving up
    if y > 0:
        # Only move left if it is not a rock
        if parsed_data[x][y-1] != "#" and not seen_positions[x][y-1][odd_even]:
            # Also set if we are at an odd or even move
            seen_positions[x][y-1][odd_even] = True
            next_positions.append([next_odd_even, x, y-1])

    # Try moving down
    if y < (grid_size -1 + grid_size * 2 * expansion_factor):
        # Only move left if it is not a rock
        if parsed_data[x][y+1] != "#" and not seen_positions[x][y+1][odd_even]:
            # Also set if we are at an odd or even move
            seen_positions[x][y+1][odd_even] = True
            next_positions.append([next_odd_even, x, y+1])
    return next_positions

# How to get the extrapolation formula for real data 
# number of steps (-1) to check [850, 1112, 1374, 1636]
# solutions that we are going to check [638049, 1090819, 1664269, 2358399]
# Differences [452770, 573450, 694130]
# Differences of differences [120680, 120680] Input 120680 in the formula as last variable
# num before 638049 is 305959  (638049 - (1090819-638049) + 120680)
# num before 305959 is 94549.  (305959 - (638049-305959)+ 120680)  Input 94549 in the middle part of the formula
# When using this formula we start from 305959 which is the solution at position 588 (2*grid_size*2 + remaining_num_steps-1)
def extrapolation_formula(input_number, two_grid_size_steps):
    x = two_grid_size_steps 
    return (x + 1) * input_number - x * 94549 + int((x+1) * x / 2) * 120680

# Dummy data
# number of steps (-1) to check [71, 93, 115, 137]
# Solutions that we are going to check [3380, 5814, 8896, 12626]
# Differences [2434, 3082, 3730]
# Differences of differences [648, 648]. Input 648 in the formula as last variable
# num before 3380 is 1594 (3380-(5814-3380) + 648)
# num before 1594 is 456 (1594 - (3380-1594) + 648). Input 456 in the middle part of the formula
# When using this formula we start from  1594, which is the solution at position 49 (2*grid_size*2 + remaining_num_steps-1)
def extrapolation_formula_dummy_data(input_number, two_grid_size_steps):
    x = two_grid_size_steps 
    return (x + 1) * input_number - x * 456 + int((x+1) * x / 2) * 648

# A seen position starts at {"odd": False, "even": False} and sets to True when it has been reached

# Part A
# num_steps = 64
# expansion_factor = 1
num_steps = grid_size * 2 * 7 + 1
expansion_factor = 2*7
parsed_data, start_position = expandStartGrid(parsed_data, start_position, expansion_factor)
seen_positions = [ [{"odd": False, "even": False} for x in range(grid_size + grid_size * 2 * expansion_factor )] for y in range(grid_size + grid_size * 2 * expansion_factor) ]

print("Number of steps", num_steps)

current_positions = [["even"] + start_position]
solutions = []
steps = range(num_steps)
for step in range(num_steps):
    print("step", step)
    next_positions = []
    for position in current_positions:
        a = getNextPositions(position, expansion_factor)
        next_positions.extend(a)
    current_positions = next_positions

    end_odd_even = "even" if (step % 2 == 0) else "odd"
    garden_plots_reachable = 0
    for col in seen_positions:
        for x in col:
            if x[end_odd_even]:
                garden_plots_reachable += 1
    solutions.append(garden_plots_reachable)

num_steps_total = 26501365
steps_divided_by_2_grid = math.floor(num_steps_total / (2 * grid_size))   # This is 101150
remaining_num_steps = num_steps_total % (2 * grid_size)                 # This is 65
# These are the dummy data inputs
# num_steps_total = 5000
# steps_divided_by_2_grid = math.floor(num_steps_total / (2 * grid_size))   # This is 227
# remaining_num_steps = num_steps_total % (2 * grid_size)   

solutions_to_check = [ remaining_num_steps - 1 + grid_size *(i*2) for i in range(3,7)]
garden_plot_solutions = [ solutions[check] for check in solutions_to_check]
print("number of steps (-1) to check", solutions_to_check)
print("solutions that we are going to check", garden_plot_solutions)

# answerA = solutions[num_steps -1]
# print("Answer A", answerA)
# submit(answerA, part="a", day=day, year=year)

new_sequence = garden_plot_solutions
while not checkAllZeroes(new_sequence):
    new_sequence = getDifferences(new_sequence)
    print(new_sequence)

### Part B ###

# Dummy data
# num_to_extrapolate_from = solutions[2*grid_size*2 + remaining_num_steps-1]
# print("Extrapolate form this should be 1594", num_to_extrapolate_from)
# num_5000 = extrapolation_formula_dummy_data(num_to_extrapolate_from, steps_divided_by_2_grid - 2)  # We need to take 101.146 extra 2x grid steps
# print("Dummy data solution for 5000 steps", num_5000)

num_to_extrapolate_from = solutions[2*grid_size*2 + remaining_num_steps-1]
# num_to_extrapolate_from = 305959
# print("Extrapolate form this should be 305959", num_to_extrapolate_from)
num_265016365 = extrapolation_formula(num_to_extrapolate_from, steps_divided_by_2_grid - 2)  # We need to take 101.146 extra 2x grid steps
print("Solution for 265016365 steps", num_265016365)
answerB = num_265016365

submit(answerB, part="b", day=day, year=year)