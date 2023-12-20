from aocd import get_data, submit

year, day = 2023, 18
data = get_data(year=year, day=day).splitlines()

def getNextCorner(previous_corner, direction, step):
    previous_x, previous_y = previous_corner[0], previous_corner[1]
    if direction =="L":
        next_corner = [ previous_x - step, previous_y]
    elif direction =="R":
        next_corner = [ previous_x + step, previous_y]
    elif direction =="D":
        next_corner = [ previous_x, previous_y + step]
    elif direction =="U":
        next_corner = [ previous_x, previous_y - step]
    else:
        print("Unkown direction")
    return next_corner

def getDeterminant(next_corner, previous_corner):
    return previous_corner[0] * next_corner[1] - next_corner[0] * previous_corner [1]

def getDistance(next_corner, previous_corner):
    return abs(next_corner[0] - previous_corner[0]) + abs( next_corner[1] - previous_corner[1])

def colorToDirection(color):
    if color == "0":
        return "R"
    elif color == "1":
        return "D"
    elif color == "2":
        return "L"
    elif color =="3":
        return "U"

directions = []
steps = []
colors = []
for row in data:
    direction, step, color = row.split(" ")
    # Part A
    # directions.append(direction)
    # steps.append(int(step))
    colors.append(color)
    # Part B
    steps.append(int(color[2:-2], 16))
    directions.append(colorToDirection(color[-2]))

previous_corner = [0,0]
corners = [[0,0]]
for direction, step in zip(directions, steps):
    next_corner = getNextCorner(previous_corner, direction, step)
    corners.append(next_corner)
    previous_corner = next_corner

area = 0
num_exterior_points = 0
previous_corner = [0,0]
for corner in corners:
    num_exterior_points += getDistance(corner, previous_corner)
    area += 0.5 * getDeterminant(corner, previous_corner)
    previous_corner = corner

num_points_in_area = area + 1 - (num_exterior_points / 2)
total_points = int(num_points_in_area + num_exterior_points)


answerA = total_points
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
answerB = total_points
submit(answerB, part="b", day=day, year=year)