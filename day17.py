from aocd import get_data, submit
import math
import time

t0 = time.time()

data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split("\n")
# data = """2413
# 3215
# 3255
# 3446""".split("\n")
year, day = 2023, 17
data = get_data(year=year, day=day).splitlines()
grid_size = len(data)

data_numbers = []
for row in data:
    data_numbers_row = []
    for block in row:
        data_numbers_row.append(int(block))
    data_numbers.append(data_numbers_row)

min_heat_loss_threshold = 3

def getNextInputs(current_position, current_heat_loss, path):
    current_x = current_position[0]
    current_y = current_position[1]
    next_positions = []
    next_heat_losses = []
    next_paths = []
    # Check the last direction, if this is the first entry the last direction is unknown (set to x)
    last_direction = path[-1] if len(path) > 0 else "x"
    # Get next left position  if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_x > 0) and path[-3:] != "lll" and last_direction != "r":
        next_x = current_x - 1
        next_y = current_y
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_three_directions = path[-2:]+"l"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_three_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_three_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold

        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_three_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "l")
    
    # Get next right position if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_x < grid_size - 1) and path[-3:] != "rrr" and last_direction != "l":
        next_x = current_x + 1
        next_y = current_y
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_three_directions = path[-2:]+"r"
        next_found_paths = found_paths[next_y][next_x]
        
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_three_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_three_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold

        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_three_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "r")
    
    # Get next up position if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_y > 0) and path[-3:] != "uuu" and last_direction != "d":
        next_x = current_x
        next_y = current_y -1
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_three_directions = path[-2:]+"u"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_three_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_three_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold

        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_three_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "u")
   
    # Get next down position, if we are not at the edge or have moved this direction three times in a row, or the previous direction was the opposite direction
    if (current_y < grid_size -1) and path[-3:] !="ddd" and last_direction != "u":
        next_x = current_x
        next_y = current_y + 1
        next_heat_loss = current_heat_loss + data_numbers[next_y][next_x] 
        next_three_directions = path[-2:]+"d"
        next_found_paths = found_paths[next_y][next_x]
        if len(next_found_paths) == 0:
            min_heat_loss = 0
        elif next_three_directions in next_found_paths:
            min_heat_loss = next_found_paths[next_three_directions]
        else:
            # Get the minimal heat loss of all possible paths
            min_heat_loss = next_found_paths[min(next_found_paths, key=next_found_paths.get)]
            min_heat_loss += min_heat_loss_threshold
        
        if min_heat_loss == 0 or (next_heat_loss < min_heat_loss ):
            found_paths[next_y][next_x][next_three_directions] = next_heat_loss
            next_positions.append([next_x, next_y])
            next_heat_losses.append(next_heat_loss)
            next_paths.append(path + "d")

    return next_positions, next_heat_losses, next_paths

def listDuplicates(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def removeDuplicatesPaths(current_positions, current_heat_losses, current_paths):
    positions_with_last_path = []
    for position, path in zip(current_positions, current_paths):
        joined_list = position + [path[-3:]]
        positions_with_last_path.append(joined_list)
    indexes_to_remove = []
    # Get all unique positions where the last three path items are the same    
    unique_positions_with_last_path = [list(x) for x in set(tuple(x) for x in positions_with_last_path)]
    for position_with_last_path in unique_positions_with_last_path:
        # Find the indices of all these similar paths
        unique_indices = listDuplicates(unique_positions_with_last_path, position_with_last_path)
        indexes_to_remove.extend(unique_indices)
        
        # Get the lowest heat loss
        poss_heat_losses = []
        for indice in unique_indices:
            poss_heat_losses.append(current_heat_losses[indice])
        
        # Append a new item with only the lowest heat loss, remove all others later on    
        current_positions.append(current_positions[unique_indices[0]])
        current_heat_losses.append(min(poss_heat_losses))
        current_paths.append(current_paths[unique_indices[0]])
    
    # Remove all the duplicate indices 
    for index in sorted(indexes_to_remove, reverse=True):
        del current_positions[index]
        del current_heat_losses[index]
        del current_paths[index]

    
    return current_positions, current_heat_losses, current_paths

current_positions = [[0,0]]
current_heat_losses = [0]
end_position = [grid_size - 1, grid_size - 1]
current_paths = [""]
minimum_heat_losses = [[0 for x in range(grid_size)] for y in range(grid_size)]
found_paths = [[{} for x in range(grid_size)] for y in range(grid_size)]
possible_heat_losses = []
possible_paths = []

# for i in range(180):
for i in range(grid_size * 3):
    new_current_positions = []
    new_heat_losses = []
    new_paths = []
    t_last_it = time.time()
    print("ITERATION", i)
    for position, heat_loss, path in zip(current_positions, current_heat_losses, current_paths):
        next_positions, next_heat_losses, next_paths = getNextInputs(position, heat_loss, path)
        # print("Input position, direction", position, path)
        # print("New positions", next_positions)
        # print("New heat losses", next_heat_losses)
        # print("New paths", next_paths)
        # print('')

        new_current_positions.extend(next_positions)
        new_heat_losses.extend(next_heat_losses)
        new_paths.extend(next_paths)
        for position_idx, next_position in enumerate(next_positions):
            if next_position == end_position:
                possible_heat_losses.append(next_heat_losses[position_idx])
                possible_paths.append(next_paths[position_idx])

    # Remove all duplicate positions where the last three directions are similar
    new_current_positions, new_heat_losses, new_paths = removeDuplicatesPaths(new_current_positions, new_heat_losses, new_paths)
                
    current_positions = new_current_positions
    current_heat_losses = new_heat_losses
    current_paths = new_paths
    print("Iteration time", time.time() - t_last_it)


answerA = min(possible_heat_losses)
print("Answer A is", answerA)
print("Number of possible solutions", len(possible_paths))
t1 = time.time()
total_time = t1-t0
print("This took", total_time)
submit(answerA, part="a", day=day, year=year)

#

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)
