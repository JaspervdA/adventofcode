from aocd import get_data, submit
import time
import copy

year, day = 2023, 23
data = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".split("\n")
# data = get_data(year=year, day=day).splitlines()
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

threshold = 1
def getNextPositions(current_position, seen_positions, hike_length):
    x, y, next_positions, next_seen_positions, next_hike_lengths = current_position[0], current_position[1], [], [], []
    # Try moving left if we are not at the edge and position not seen before
    new_seen_positions = copy.deepcopy(seen_positions)
    new_seen_positions[x][y] = True
    if x > 0:
        next_x, next_y = x-1, y
        if not seen_positions[next_x][next_y]:
            if hiking_map[next_x][next_y] == "<":
                next_seen_positions.append(new_seen_positions), 
                next_positions.append([next_x-1, next_y])
                next_hike_lengths.append(hike_length + 2)
            elif hiking_map[next_x][next_y] == "." and (hike_length + 1 + threshold) > longest_path_at_each_position[next_x][next_y]:
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x, next_y])
                next_hike_lengths.append(hike_length + 1)
                if (hike_length + 1) > longest_path_at_each_position[next_x][next_y]:
                    longest_path_at_each_position[next_x][next_y] = hike_length + 1
     # Try moving right if we are not at the edge and position not seen before
    if x < (grid_size - 1):
        next_x, next_y = x+1, y
        if not seen_positions[next_x][next_y]:
            if hiking_map[next_x][next_y] == ">":
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x+1, next_y])
                next_hike_lengths.append(hike_length + 2)
            elif hiking_map[next_x][next_y] == "." and (hike_length + 1 + threshold) > longest_path_at_each_position[next_x][next_y]:
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x, next_y])
                next_hike_lengths.append(hike_length + 1)
                if (hike_length + 1) > longest_path_at_each_position[next_x][next_y]:
                    longest_path_at_each_position[next_x][next_y] = hike_length + 1
    # Try moving up if we are not at the edge and position not seen before
    if y > 0:
        next_x, next_y = x, y-1
        if not seen_positions[next_x][next_y]:
            if hiking_map[next_x][next_y] == "^":
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x, next_y -1])
                next_hike_lengths.append(hike_length + 2)
            elif hiking_map[next_x][next_y] == "." and (hike_length + 1 + threshold) > longest_path_at_each_position[next_x][next_y]:
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x, next_y])
                next_hike_lengths.append(hike_length + 1)
                if (hike_length + 1) > longest_path_at_each_position[next_x][next_y]:
                    longest_path_at_each_position[next_x][next_y] = hike_length + 1
     # Try moving down if we are not at the edge and position not seen before
    if y < (grid_size - 1):
        next_x, next_y = x, y+1
        if not seen_positions[next_x][next_y]:
            if hiking_map[next_x][next_y] == "v":
                next_seen_positions.append(new_seen_positions)
                next_positions.append([next_x, next_y+1])
                next_hike_lengths.append(hike_length + 2)
            elif hiking_map[next_x][next_y] == "." and (hike_length + 1 + threshold) > longest_path_at_each_position[next_x][next_y]:
                next_positions.append([next_x, next_y])
                next_seen_positions.append(new_seen_positions)
                next_hike_lengths.append(hike_length + 1)
                if (hike_length + 1) > longest_path_at_each_position[next_x][next_y]:
                    longest_path_at_each_position[next_x][next_y] = hike_length + 1

    return next_positions, next_seen_positions, next_hike_lengths

current_position_list, current_hike_lengths = [[1,0]], [0]
current_seen_positions_list = [[[False for x in range(grid_size)] for y in range(grid_size)]]
total_hike_lengths, step = [], 0
longest_path_at_each_position = [[0 for x in range(grid_size)] for y in range(grid_size)]
t_start = time.time()
while len(current_position_list) > 0:
# for i in range(800):
    step +=1
    # step = i
    print("Step", step)
    new_current_positions, new_seen_positions, new_hike_lengths = [], [], []
    t_last_it = time.time()
    for current_position, seen_positions, hike_length in zip(current_position_list, current_seen_positions_list, current_hike_lengths):
        if current_position == [grid_size - 2, grid_size - 1]:    
            total_hike_lengths.append(hike_length)
        else:
            # print("current position", current_position)
            next_positions, next_seen_positions, next_hike_lengths = getNextPositions(current_position, seen_positions, hike_length)
            new_current_positions.extend(next_positions), new_seen_positions.extend(next_seen_positions), new_hike_lengths.extend(next_hike_lengths)

    current_position_list, current_seen_positions_list, current_hike_lengths = new_current_positions, new_seen_positions, new_hike_lengths
    print("Number of positions", len(current_position_list))
    print("Iteration time", time.time() - t_last_it)


print("Total loop time", time.time() - t_start)
print("Hike lengths", total_hike_lengths)
answerA = max(total_hike_lengths)
print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)