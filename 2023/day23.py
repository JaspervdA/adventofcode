from aocd import get_data, submit
import time
import sys

year, day = 2023, 23
data = get_data(year=year, day=day).splitlines()
grid_size = len(data)
hiking_map = [[None for x in range(grid_size)] for y in range(grid_size)]
for y, row in enumerate(data):
    for x, col in enumerate(row):
        # Part A
        # hiking_map[x][y] = col
        # If statement for part B
        if col == ">" or col == "<" or col == "^" or col =="v":
            hiking_map[x][y] = "."
        else:
            hiking_map[x][y] = col

def getPossiblePositions(x, y, seen_positions, last_position):
    possible_positions, next_positions = [], []
    # Check if left is possible
    if x > 0:
        next_x, next_y = x-1, y
        next_x_y_string = f"{next_x},{next_y}"
        if (f";{next_x_y_string};" not in seen_positions) and (next_x_y_string != last_position) and (hiking_map[next_x][next_y] == "<" or hiking_map[next_x][next_y] == "."):
            possible_positions.append("l")
            next_positions.append(next_x_y_string)
    # Check if right is possible
    if x < (grid_size - 1):
        next_x, next_y = x+1, y
        next_x_y_string = f"{next_x},{next_y}"
        if (f";{next_x_y_string};" not in seen_positions) and (next_x_y_string != last_position) and (hiking_map[next_x][next_y] == ">" or hiking_map[next_x][next_y] == "."):
            possible_positions.append("r")
            next_positions.append(next_x_y_string)
    # Check if up is possible
    if y > 0:
        next_x, next_y = x, y-1
        next_x_y_string = f"{next_x},{next_y}"
        if (f";{next_x_y_string};" not in seen_positions) and (next_x_y_string != last_position) and (hiking_map[next_x][next_y] == "^" or hiking_map[next_x][next_y] == "."):
            possible_positions.append("u")
            next_positions.append(next_x_y_string)
    # Check if down is possible
    if y < (grid_size - 1):
        next_x, next_y = x, y+1
        next_x_y_string = f"{next_x},{next_y}"
        if (f";{next_x_y_string};" not in seen_positions) and (next_x_y_string != last_position) and (hiking_map[next_x][next_y] == "v" or hiking_map[next_x][next_y] == "."):
            possible_positions.append("d")
            next_positions.append(next_x_y_string)
    return possible_positions, next_positions

def getNextPositions(loop_item):
    current_position, seen_positions, hike_length, last_position = loop_item[0], loop_item[1], loop_item[2], loop_item[3]
    next_loop_items, next_hike_lengths = [], []
    x,y = current_position.split(',')
    x, y = int(x), int(y)
    possible_positions, next_positions = getPossiblePositions(x, y, seen_positions, last_position)
    num_possible_positions = len(possible_positions)
    if num_possible_positions == 0:
        return []
    elif num_possible_positions == 1:
        next_loop_items = [[None, seen_positions, hike_length+1, current_position]]
    else:
        next_loop_items = [[None, f"{seen_positions}{x},{y};", hike_length+1, current_position] for i in range(num_possible_positions)]

    for loop_item, next_position in zip(next_loop_items, next_positions):
        loop_item[0] = next_position

    return next_loop_items

# Loop data is current_position, seen_positions, hike_length, last_position
current_loop_data = [['1,0', ';', 0, '0,0']]
total_hike_lengths, step, end_position = [], 0, f"{grid_size - 2},{grid_size - 1}"
t_start = time.time()
while len(current_loop_data) > 0:
    step +=1
    print("Step", step)
    new_loop_data = []
    t_last_it = time.time()
    for loop_item in current_loop_data:
        if loop_item[0] == end_position:    
            total_hike_lengths.append(loop_item[2])
            del loop_item
        else:
            next_loop_data = getNextPositions(loop_item)
            if len(next_loop_data) > 0:
                new_loop_data.extend(next_loop_data)
            else:
                del next_loop_data, loop_item

    current_loop_data = new_loop_data
    print("Number of positions", len(current_loop_data))
    print("Iteration time", time.time() - t_last_it)

print("Total loop time", time.time() - t_start)
# print("Hike lengths", total_hike_lengths)
answerA = max(total_hike_lengths)
print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
answerB = 6442
#  5314 is too low!!
submit(answerB, part="b", day=day, year=year)