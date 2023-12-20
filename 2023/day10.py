from aocd import get_data, submit
import numpy as np

year, day = 2023, 10
data = get_data(year=year, day=day).splitlines()

for y, row in enumerate(data):
    for x, col in enumerate(row):
        if col =="S":
            start_x = x
            start_y = y

# Get the next pipe
def getNextPipe(current_y, current_x, current_direction):
    new_y = current_y
    new_x = current_x
    new_direction = current_direction
    if current_direction == "South":
        new_y = current_y + 1
        new_pipe = data_matrix[new_y][new_x]
        if new_pipe == "L":
            new_direction = "East"
        elif new_pipe == "J":
            new_direction = "West"

    elif current_direction == "North":
        new_y = current_y - 1
        new_pipe = data_matrix[new_y][new_x]
        if new_pipe == "F":
            new_direction = "East"
        elif new_pipe == "7":
            new_direction = "West"

    elif current_direction == "West":
        new_x = current_x - 1
        new_pipe = data_matrix[new_y][new_x]
        if new_pipe == "L":
            new_direction = "North"
        elif new_pipe == "F":
            new_direction = "South"

    elif current_direction == "East":
        new_x = current_x + 1
        new_pipe = data_matrix[new_y][new_x]
        if new_pipe == "J":
            new_direction = "North"
        elif new_pipe == "7":
            new_direction = "South"
    else:
        print("Something went wrong in getting the next pipe")

    return new_y, new_x, new_direction, new_pipe

data_matrix = np.array(data)
# Get the next 2 pipes
north_pipe = data_matrix[start_y-1][start_x]
south_pipe = data_matrix[start_y+1][start_x]
# Out of bounds
west_pipe = data_matrix[start_y][start_x -1]
east_pipe = data_matrix[start_y][start_x +1]

#Start with the south pipe
current_y = start_y + 1
current_x = start_x
direction = "South"

new_pipe = "|"
pipe_values = []
pipe_value = 0

new_y = start_y
new_x = start_x
new_direction = "South"
new_matrix = np.full((data_matrix.size, data_matrix.size), "." )
# new_matrix = np.full((10, 20), "." )

corners = [[start_x,start_y]]
while new_pipe != "S":
    pipe_value += 1
    corners.append([new_x,new_y])
    new_y, new_x, new_direction, new_pipe = getNextPipe(new_y, new_x, new_direction)
    new_matrix[new_y][new_x] = new_pipe
    pipe_values.append(pipe_value)
corners.append([start_x,start_y])

def ifAdjacentAllPipes(current_y, current_x):
    check = True
    for y in range(2):
        for x in range(2):
            check_y = current_y - 1 + y
            check_x = current_x - 1 + x
            if new_matrix[check_y][check_x] == ".":
                check = False
    return check
            
distance = int(max(pipe_values) / 2 )
answerA = distance
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def getDeterminant(next_corner, previous_corner):
    return previous_corner[0] * next_corner[1] - next_corner[0] * previous_corner [1]

area = 0
previous_corner = corners[0]
for corner in corners:
    # print(getDeterminant(corner, pre))
    area += 0.5 * getDeterminant(corner, previous_corner)
    previous_corner = corner

area = abs(area)
num_exterior_point = distance * 2
num_points_in_area = area + 1 - (num_exterior_point / 2)

answerB = int(num_points_in_area)
print("Answer B is", answerB)
submit(answerB, part="b", day=day, year=year)