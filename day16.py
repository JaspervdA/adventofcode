from aocd import get_data, submit
import re
import copy

year, day = 2023, 16
data = get_data(year=year, day=day).splitlines()
# data = """.|...\....
# |.-.\\.....
# .....|-...
# ........|.
# ..........
# .........\\
# ..../.\\\\..
# .-.-/..|..
# .|....-|.\\
# ..//.|....""".split("\n")

grid_size = len(data)

def transposePuzzle(puzzle_rows):
    puzzle_cols = []
    num_cols = len(puzzle_rows[0])
    for x in range(num_cols):
        puzzle_col = ""
        for puzzle_row in puzzle_rows:
            puzzle_col += puzzle_row[x]
        puzzle_cols.append(puzzle_col)
    return puzzle_cols

def reverseMirrorPositions(mirror_positions):
    reversed_positions = []
    copy.deepcopy(mirror_positions)
    for i in reversed(mirror_positions):
        reversed_positions.append(grid_size - 1 - i)

    return reversed_positions

def getNextObstacle(reverse, current_position, splitter_positions, mirrorL_positions, mirrorZ_positions):
    if reverse:
        current_position = grid_size - 1 - current_position
        splitter_positions = reverseMirrorPositions(splitter_positions)
        mirrorL_positions = reverseMirrorPositions(mirrorL_positions)
        mirrorZ_positions = reverseMirrorPositions(mirrorZ_positions)

    closest_splitter_position = grid_size
    closest_mirrorL_position = grid_size
    closest_mirrorZ_position = grid_size
    for splitter_position in splitter_positions:
        if current_position < splitter_position:
            closest_splitter_position = splitter_position
            break
    for mirrorL_position in mirrorL_positions:
        if current_position < mirrorL_position:
            closest_mirrorL_position = mirrorL_position
            break
    for mirrorZ_position in mirrorZ_positions:
        if current_position < mirrorZ_position:
            closest_mirrorZ_position = mirrorZ_position
            break
    
    obstacle_position = min(closest_splitter_position, closest_mirrorL_position, closest_mirrorZ_position)
    if obstacle_position == grid_size:
        return None, grid_size

    if obstacle_position == closest_splitter_position:
        obstacle_type = "splitter"
    elif obstacle_position == closest_mirrorL_position:
        obstacle_type = "mirrorL"
    elif obstacle_position == closest_mirrorZ_position:
        obstacle_type = "mirrorZ"
    else:
        print("something went wrong in finding the closest obstacle")

    if reverse: 
        obstacle_position = grid_size - 1 - obstacle_position
    return obstacle_type, obstacle_position

splitter_row_positions = []
mirrorL_row_positions = []
mirrorZ_row_positions = []
for row in data:
    splitter_row_positions.append( [m.start() for m in re.finditer(re.escape("|"), row)] )
    mirrorL_row_positions.append( [m.start() for m in re.finditer(re.escape("\\"), row)] )
    mirrorZ_row_positions.append( [m.start() for m in re.finditer(re.escape("/"), row)] )

splitter_col_positions = []
mirrorL_col_positions = []
mirrorZ_col_positions =[]
for col in transposePuzzle(data):
    splitter_col_positions.append( [m.start() for m in re.finditer(re.escape("-"), col)] )
    mirrorL_col_positions.append( [m.start() for m in re.finditer(re.escape("\\"), col)] )
    mirrorZ_col_positions.append( [m.start() for m in re.finditer(re.escape("/"), col)] )

def getNextDirectionsAndPosition(beam_direction, current_position):
    if beam_direction == "r" or beam_direction == "l":
        reverse = beam_direction == "l"
        obstacle_type, obstacle_position = getNextObstacle(reverse, current_position[0], splitter_row_positions[current_position[1]], mirrorL_row_positions[current_position[1]], mirrorZ_row_positions[current_position[1]])
        # Als de obstacle position de grid size is, dus 10 in dummy data hebben dan schiet de beam eigenlijk buiten het veld
        if obstacle_position == grid_size and beam_direction == "r":
            return [], [grid_size -1  ,current_position[1]]
        elif obstacle_position == grid_size and beam_direction == "l":
            return [], [0 ,current_position[1]]
        
        if obstacle_type == "splitter":
            next_beam_directions = ["d","u"]
        elif obstacle_type == "mirrorZ" and beam_direction == "r":
            next_beam_directions = ["u"]
        elif obstacle_type == "mirrorZ" and beam_direction == "l":
            next_beam_directions = ["d"]
        elif obstacle_type == "mirrorL" and beam_direction == "r":
            next_beam_directions = ["d"]
        elif obstacle_type == "mirrorL" and beam_direction == "l":
            next_beam_directions = ["u"]
        else:
            print("Unkonwn obsctable type and beam direction combination")
        next_position = [obstacle_position, current_position[1]]
    
    elif beam_direction == "d" or beam_direction =="u":
        reverse = beam_direction == "u"
        obstacle_type, obstacle_position = getNextObstacle(reverse, current_position[1], splitter_col_positions[current_position[0]], mirrorL_col_positions[current_position[0]], mirrorZ_col_positions[current_position[0]])
        # Als de obstacle position de grid size is, dus 10 in dummy data hebben dan schiet de beam eigenlijk buiten het veld
        if obstacle_position == grid_size and beam_direction == "d":
            return [], [current_position[0], grid_size - 1]
        elif obstacle_position == grid_size and beam_direction == "u":
            return [], [current_position[0], 0]
        
        if obstacle_type == "splitter":
            next_beam_directions = ["r","l"]
        elif obstacle_type == "mirrorZ" and beam_direction == "d":
            next_beam_directions = ["l"]
        elif obstacle_type == "mirrorZ" and beam_direction == "u":
            next_beam_directions = ["r"]
        elif obstacle_type == "mirrorL" and beam_direction == "d":
            next_beam_directions = ["r"]
        elif obstacle_type == "mirrorL" and beam_direction == "u":
            next_beam_directions = ["l"]
        else:
            print("Unknown obsctable type and beam direction combination")
        next_position = [current_position[0], obstacle_position]
    else:
        print("Unknown beam direction")

    return next_beam_directions, next_position

def setTravelledFieldsToOne(next_position, current_position, grid):
    x_diff = next_position[0] - current_position[0]
    y_diff = next_position[1] - current_position[1]
    
    if x_diff == 0 and y_diff == 0:
        return
    elif x_diff == 0:
        for y in range(abs(y_diff)+1):
            start_y = current_position[1] if y_diff > 0 else next_position[1]
            # grid[y + start_y][current_position[0]] = 1
            grid[min(y + start_y,grid_size -1)][current_position[0]] = 1
        return
    elif y_diff == 0:
        for x in range(abs(x_diff)+1):
            start_x = current_position[0] if x_diff > 0 else next_position[0]
            # grid[current_position[1]][start_x + x] = 1
            grid[current_position[1]][min(start_x + x,grid_size - 1)] = 1
        return


current_beam_direction = "r" # can be u,d,l,r --> up, down, left, right
current_position = [-1,0]
possible_paths = [[current_beam_direction, current_position]]
already_seen_paths = []
empty_grid = [[0 for i in range(grid_size)] for l in range(grid_size)]

while len(possible_paths) > 0:
    new_possible_paths = []
    for possible_path in possible_paths:
        next_beam_directions, next_position = getNextDirectionsAndPosition(possible_path[0], possible_path[1])
        setTravelledFieldsToOne(next_position, possible_path[1], empty_grid)

        for next_beam_direction in next_beam_directions:
            if [next_beam_direction, next_position] in already_seen_paths:
                continue
            else:
                new_possible_paths.append([next_beam_direction, next_position])
                already_seen_paths.append([next_beam_direction, next_position])
    possible_paths = new_possible_paths

distance_travelled = -1
for row in empty_grid:
    distance_travelled += sum(row)

answerA = distance_travelled
# print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def runStartPositions(start_position, start_beam_direction):
    current_beam_direction = start_beam_direction # can be u,d,l,r --> up, down, left, right
    current_position = start_position
    possible_paths = [[current_beam_direction, current_position]]
    already_seen_paths = []
    empty_grid = [[0 for i in range(grid_size)] for l in range(grid_size)]
    while len(possible_paths) > 0:
        new_possible_paths = []
        for possible_path in possible_paths:
            next_beam_directions, next_position = getNextDirectionsAndPosition(possible_path[0], possible_path[1])
            setTravelledFieldsToOne(next_position, possible_path[1], empty_grid)

            for next_beam_direction in next_beam_directions:
                if [next_beam_direction, next_position] in already_seen_paths:
                    continue
                else:
                    new_possible_paths.append([next_beam_direction, next_position])
                    already_seen_paths.append([next_beam_direction, next_position])
        possible_paths = new_possible_paths
    distance_travelled = 0
    
    for row in empty_grid:
        # print(row)
        distance_travelled += sum(row)
    return distance_travelled

start_positions_top = [[i,-1] for i in range(grid_size)]
start_positions_bottom = [[i,grid_size] for i in range(grid_size)]
start_positions_left = [[-1,i] for i in range(grid_size)]
start_positions_right = [[grid_size,i] for i in range(grid_size)]

energized_tiles = []
i = 0
for start_position_top, start_position_bottom, start_position_left, start_position_right in zip(start_positions_top, start_positions_bottom, start_positions_left, start_positions_right):
    energized_tiles.append(runStartPositions(start_position_top, "d"))
    energized_tiles.append(runStartPositions(start_position_bottom, "u"))
    energized_tiles.append(runStartPositions(start_position_left, "r"))
    energized_tiles.append(runStartPositions(start_position_right, "l"))

# energized_tiles.append(runStartPositions([1,-1], "d"))

print(energized_tiles)
answerB = max(energized_tiles)
print("Answer B is", answerB)
# 7487 is too low!!!

submit(answerB, part="b", day=day, year=year)