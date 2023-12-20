from aocd import get_data, submit
import math
import time

t0 = time.time()

# data = """2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533""".split("\n")

# The data below is a test case for part B
# data = """2413432311323
# 3215453535623
# 9255995654254
# 9446985845452
# 9546657867536
# 9438598798454
# 4457876987766
# 3637877979653
# 4654967911117
# 4564679916459
# 1224686815569
# 2546548817739
# 4322674611113""".split("\n")
year, day = 2023, 17
data = get_data(year=year, day=day).splitlines()
grid_size = len(data)

#Compute the average heat loss per field
data_numbers = []
for row in data:
    data_numbers_row = []
    for block in row:
        data_numbers_row.append(int(block))
    data_numbers.append(data_numbers_row)

min_heat_loss_threshold = 20

def getNextInputs(current_position, current_heat_loss, path):
    current_x = current_position[0]
    current_y = current_position[1]
    next_positions = []
    next_heat_losses = []
    next_paths = []
    # Check the last direction, if this is the first entry the last direction is unknown (set to x)
    last_direction = path[-1] if len(path) > 0 else "x"
    last_four_directions = path[-4:] if len(path) > 3 else "xxxx"
    last_ten_directions = path[-10:] if len(path) > 9 else "xxxxxxxxxx"
    # Get next left position  if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if last_direction == "l":
        next_direction = "x" if (last_four_directions == "llll") else "l"
    elif last_direction == "r":
        next_direction = "x" if (last_four_directions == "rrrr") else "r"
    elif last_direction == "d":
        next_direction = "x" if (last_four_directions == "dddd") else "d"
    elif last_direction == "u":
        next_direction = "x" if (last_four_directions == "uuuu") else "u"   
    elif last_direction =="x":
        next_direction = "x"
    # If we are closer than 3 to the egde go to the edge
    # if (grid_size - current_x) < 5 and (grid_size - current_x - 1) != 0 :
    #     next_direction = "r"
    # elif (grid_size - current_y) < 5 and (grid_size - current_y - 1) != 0:
    #     next_direction = "d"
    
    can_go_left = next_direction == "l" or next_direction =="x"
    # Get next left position if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_x > 0) and last_ten_directions != "llllllllll" and last_direction != "r" and can_go_left:
        next_x = current_x - 1
        next_y = current_y
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_ten_directions = path[-13:]+"l"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_ten_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_ten_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold

        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_ten_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "l")
    
    can_go_right = next_direction == "r" or next_direction =="x"
    # Get next right position if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_x < grid_size - 1) and last_ten_directions != "rrrrrrrrrr" and last_direction != "l" and can_go_right:
        next_x = current_x + 1
        # If the next step is moving to the edge and we did not get there with 3 right steps:
        if next_x == (grid_size -1) and last_four_directions[-3:] != "rrr":
            return next_positions, next_heat_losses, next_paths
        next_y = current_y
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_ten_directions = path[-13:]+"r"
        next_found_paths = found_paths[next_y][next_x]
        
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_ten_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_ten_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold


        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_ten_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "r")
    
    can_go_up = (next_direction == "u" or next_direction =="x")
    # Get next up position if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_y > 0) and last_ten_directions != "uuuuuuuuuu" and last_direction != "d" and can_go_up:
        next_x = current_x
        next_y = current_y -1
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_ten_directions = path[-13:]+"u"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_ten_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_ten_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold

        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_ten_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "u")
   
    can_go_down = next_direction == "d" or next_direction =="x"
    # Get next down position, if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_y < grid_size -1) and last_ten_directions !="dddddddddd" and last_direction != "u" and can_go_down:
        next_x = current_x
        next_y = current_y + 1
        # If the next step is moving to the edge and we did not get there with 3 down steps:
        if next_y == (grid_size -1) and last_four_directions[-3:] != "ddd":
            return next_positions, next_heat_losses, next_paths
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_ten_directions = path[-13:]+"d"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_ten_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_ten_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold
        
        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_ten_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "d")

    return next_positions, next_heat_losses, next_paths

current_positions = [[0,0]]
current_heat_losses = [0]
current_paths = [""]
found_paths = [[{} for x in range(grid_size)] for y in range(grid_size)]
end_position = [grid_size - 1, grid_size - 1]
possible_heat_losses = []
possible_paths = []
# solution_path = "rrrrrrrrddddrrrrddddllllddddrrrr"
# solution_path = "rrrrrrrrrr"

for i in range(grid_size * 3):
# for i in range(12):
    new_current_positions = []
    new_heat_losses = []
    new_paths = []
    t_last_it = time.time()
    print("ITERATION", i)
    for position, heat_loss, path in zip(current_positions, current_heat_losses, current_paths):
        next_positions, next_heat_losses, next_paths = getNextInputs(position, heat_loss, path)
        new_current_positions.extend(next_positions)
        new_heat_losses.extend(next_heat_losses)
        new_paths.extend(next_paths)
        # if path[:-1] == solution_path[:len(path) -1]:
        #     print("Input position, direction", position, path)
        #     print("New positions", next_positions)
        #     print("New heat losses", next_heat_losses)
        #     print("New paths", next_paths)
        #     print('')
        for position_idx, next_position in enumerate(next_positions):
            if next_position == end_position:
                possible_heat_losses.append(next_heat_losses[position_idx])
                possible_paths.append(next_paths[position_idx])

    # Should we remove duplicate positions and take the one with the lowest score?
    current_positions = new_current_positions
    current_heat_losses = new_heat_losses
    current_paths = new_paths
    print("Iteration time", time.time() - t_last_it)


min_index = possible_heat_losses.index(min(possible_heat_losses))
solution_path = possible_paths[min_index]
answerB = min(possible_heat_losses)
print("Solution path is", solution_path)
print("Answer B is", answerB)
print("Number of possible solutions", len(possible_paths))
t1 = time.time()
total_time = t1-t0
print("This took", total_time)
# Answer 635 is too low!
# Answer 853 is too high!
# Answer 840 is not correct :(
# Answer 794 is not correct :(
# submit(answerB, part="b", day=day, year=year)

# print(getNextInputs([10, 4], 25 , "rrrrrrddddrrrr"))